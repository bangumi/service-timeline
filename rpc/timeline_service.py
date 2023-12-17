import html
import time
from typing import Any, Optional

import phpserialize as php
import pydantic
from grpc import RpcContext
from loguru import logger
from sqlalchemy.orm import Session

from api.v1 import timeline_pb2_grpc
from api.v1.timeline_pb2 import (
    EpisodeCollectRequest,
    EpisodeCollectResponse,
    HelloRequest,
    HelloResponse,
    SubjectCollectRequest,
    SubjectCollectResponse,
    SubjectProgressRequest,
    SubjectProgressResponse,
)
from chii.compat import phpseralize
from chii.config import config
from chii.db import sa
from chii.db.tables import ChiiTimeline
from chii.timeline import (
    SUBJECT_TYPE_MAP,
    ProgressMemo,
    SubjectImage,
    SubjectMemo,
    TimelineCat,
)

BatchMeme: pydantic.TypeAdapter[dict[int, Any]] = pydantic.TypeAdapter(dict[int, Any])

BatchSubjectImage: pydantic.TypeAdapter[dict[int, Any]] = pydantic.TypeAdapter(
    dict[int, Any]
)


class TimeLineService(timeline_pb2_grpc.TimeLineServiceServicer):
    def __init__(self):
        self.SessionMaker = sa.sync_session_maker()

    def Hello(self, request: HelloRequest, context) -> HelloResponse:
        print(f"{config.node_id} rpc hello {request.name}")
        return HelloResponse(message=f"{config.node_id}: hello {request.name}")

    @logger.catch(reraise=True)
    def SubjectCollect(
        self, request: SubjectCollectRequest, context: RpcContext
    ) -> SubjectCollectResponse:
        tlType = SUBJECT_TYPE_MAP[request.subject.type][request.collection]
        if config.debug:
            print(request)
        with self.SessionMaker.begin() as session:
            tl: Optional[ChiiTimeline] = session.scalar(
                sa.get(
                    ChiiTimeline,
                    ChiiTimeline.uid == request.user_id,
                    order=ChiiTimeline.id.desc(),
                )
            )

            if tl and tl.dateline >= int(time.time() - 15 * 60):
                logger.info("find previous timeline, merging")
                if tl.cat == TimelineCat.Subject and tl.type == tlType:
                    self.merge_previous_timeline(session, tl, request)
                    return SubjectCollectResponse(ok=True)

            logger.info(
                "missing previous timeline or timeline type mismatch, create a new timeline"
            )
            self.create_subject_collection_timeline(session, request, tlType)
            session.commit()

        return SubjectCollectResponse(ok=True)

    @staticmethod
    def merge_previous_timeline(
        session: Session, tl: ChiiTimeline, req: SubjectCollectRequest
    ):
        escaped = html.escape(req.comment)
        if tl.batch:
            memo = BatchMeme.validate_python(phpseralize.loads(tl.memo.encode()))
        else:
            m = SubjectMemo.model_validate(phpseralize.loads(tl.memo.encode()))
            if int(m.subject_id) == req.subject.id:
                # save request called twice, just ignore
                should_update = False
                if m.collect_comment != escaped:
                    should_update = True
                    m.collect_comment = escaped

                if m.collect_rate != req.rate:
                    should_update = True
                    m.collect_rate = req.rate

                if should_update:
                    tl.memo = php.serialize(m.model_dump())
                    session.add(tl)
                return

            memo = {int(m.subject_id): m.model_dump()}

        memo[req.subject.id] = SubjectMemo(
            subject_id=str(req.subject.id),
            collect_comment=escaped,
            collect_rate=req.rate,
        ).model_dump()

        if tl.batch:
            img = BatchSubjectImage.validate_python(phpseralize.loads(tl.img.encode()))
        else:
            i = SubjectImage.model_validate(phpseralize.loads(tl.img.encode()))
            img = {int(i.subject_id): i.model_dump}

        img[req.subject.id] = SubjectImage(
            subject_id=str(req.subject.id), images=req.subject.image
        ).model_dump()

        tl.batch = 1
        tl.memo = php.serialize(memo)
        tl.img = php.serialize(img)

        session.add(tl)

    @staticmethod
    def create_subject_collection_timeline(
        session: Session, req: SubjectCollectRequest, type: int
    ):
        memo = SubjectMemo(
            subject_id=str(req.subject.id),
            collect_comment=html.escape(req.comment),
            collect_rate=req.rate,
        )

        img = SubjectImage(subject_id=str(req.subject.id), images=req.subject.image)

        session.add(
            ChiiTimeline(
                cat=TimelineCat.Subject,
                type=type,
                uid=req.user_id,
                memo=php.serialize(memo.model_dump()),
                img=php.serialize(img.model_dump()),
                batch=0,
                related=str(req.subject.id),
            )
        )

    @logger.catch(reraise=True)
    def EpisodeCollect(
        self, req: EpisodeCollectRequest, context
    ) -> EpisodeCollectResponse:
        """

        cat 4 type 2 "看过 ep2 ${subject name}"
        tml_id    tml_uid tml_cat tml_type tml_related
        32073511  287622  4       2        363612

        tml_memo
        a:5:{

        s:5:"ep_id";s:7:"1075441";

        s:7:"ep_name";s:0:"";

        s:7:"ep_sort";s:1:"2";

        s:10:"subject_id";s:6:"363612";

        s:12:"subject_name";s:6:"沙盒";

        }

        tml_img
        a:2:{s:10:"subject_id";s:6:"363612";s:6:"images";s:22:"82/15/363612_On6wg.jpg";}

        tml_batch  tml_source      tml_replies     tml_dateline
         0         0               0               1672520183


        cat 4 type 2 "完成了 ${subject name} {ep} of {ep_total} 话"

        memo: a:7:{

        s:9:"eps_total";s:2:"12";

        s:10:"eps_update";i:12;

        s:10:"vols_total";s:2:"??";


        s:11:"vols_update";N;

        s:10:"subject_id";s:6:"353657";

        s:12:"subject_name";s:21:"勇者、辞めます";

        s:15:"subject_type_id";s:1:"2";

        }

        """

        tlType = 2
        memo = ProgressMemo(
            ep_id=req.last.id,
            subject_name=req.subject.name,
            ep_name=req.last.name,
            subject_id=str(req.subject.id),
            subject_type_id=str(req.subject.type),
            ep_sort=req.last.sort,
        )

        img = SubjectImage(
            subject_id=str(req.subject.id),
            images=req.subject.image,
        )

        if config.debug:
            print(req)

        with self.SessionMaker.begin() as session:
            tl: Optional[ChiiTimeline] = session.scalar(
                sa.get(
                    ChiiTimeline,
                    ChiiTimeline.uid == req.user_id,
                    order=ChiiTimeline.id.desc(),
                )
            )
            if tl and tl.dateline >= int(time.time() - 15 * 60):
                logger.info("find previous timeline, updating")
                if (
                    tl.cat == TimelineCat.Progress
                    and tl.type == tlType
                    and tl.batch == 0
                    and tl.related == str(req.subject.id)
                ):
                    tl.memo = php.serialize(memo.model_dump())
                    session.add(tl)
                    return EpisodeCollectResponse(ok=True)

            session.add(
                ChiiTimeline(
                    uid=req.user_id,
                    memo=php.serialize(memo.model_dump()),
                    img=php.serialize(img.model_dump()),
                    cat=TimelineCat.Progress,
                    type=tlType,
                    source=5,
                    batch=0,
                    related=str(req.subject.id),
                )
            )
            session.commit()

        return EpisodeCollectResponse(ok=True)

    @logger.catch(reraise=True)
    def SubjectProgress(
        self, req: SubjectProgressRequest, context
    ) -> SubjectProgressResponse:
        memo = ProgressMemo(
            subject_name=req.subject.name,
            subject_id=str(req.subject.id),
            subject_type_id=str(req.subject.type),
            eps_total=str(req.subject.eps_total) if req.subject.eps_total else "??",
            vols_total=str(req.subject.vols_total) if req.subject.vols_total else "??",
            eps_update=req.eps_update,
            vols_update=req.vols_update,
        )

        tlType = 0

        img = SubjectImage(
            subject_id=str(req.subject.id),
            images=req.subject.image,
        )

        if config.debug:
            print(req)

        with self.SessionMaker.begin() as session:
            tl: Optional[ChiiTimeline] = session.scalar(
                sa.get(
                    ChiiTimeline,
                    ChiiTimeline.uid == req.user_id,
                    order=ChiiTimeline.id.desc(),
                )
            )
            if tl and tl.dateline >= int(time.time() - 15 * 60):
                logger.info("find previous timeline, updating")
                if (
                    tl.cat == TimelineCat.Progress
                    and tl.type == tlType
                    and tl.batch == 0
                    and tl.related == str(req.subject.id)
                ):
                    tl.memo = php.serialize(memo.model_dump())
                    session.add(tl)
                    session.commit()
                    return SubjectProgressResponse(ok=True)

            session.add(
                ChiiTimeline(
                    uid=req.user_id,
                    memo=php.serialize(memo.model_dump()),
                    img=php.serialize(img.model_dump()),
                    cat=TimelineCat.Progress,
                    type=tlType,
                    batch=0,
                    related=str(req.subject.id),
                )
            )
            session.commit()

        return SubjectProgressResponse(ok=True)
