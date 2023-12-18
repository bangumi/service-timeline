import html
import time
from typing import Optional

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
    SubjectMemo,
    TimelineCat,
)

BatchMeme: pydantic.TypeAdapter[dict[int, SubjectMemo]] = pydantic.TypeAdapter(
    dict[int, SubjectMemo]
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
        """
        cat 3 看过/读过/抛弃了...

        https://github.com/bangumi/dev-docs/blob/master/Timeline.md#cat_sbj_collect-条目收藏
        """
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

            if tl and tl.dateline >= int(time.time() - 10 * 60):
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

            memo = {int(m.subject_id): m}

        memo[req.subject.id] = SubjectMemo(
            subject_id=str(req.subject.id),
            collect_comment=escaped,
            collect_rate=req.rate,
            collect_id=req.collection_id,
        )

        tl.batch = 1
        tl.memo = php.serialize(
            {key: value.model_dump() for key, value in memo.items()}
        )

        session.add(tl)

    @staticmethod
    def create_subject_collection_timeline(
        session: Session, req: SubjectCollectRequest, type: int
    ):
        memo = SubjectMemo(
            subject_id=str(req.subject.id),
            collect_comment=html.escape(req.comment),
            collect_rate=req.rate,
            collect_id=req.collection_id,
        )

        session.add(
            ChiiTimeline(
                cat=TimelineCat.Subject,
                type=type,
                uid=req.user_id,
                memo=php.serialize(memo.model_dump()),
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
        """
        cat 4 type 0
        """
        tlType = 0

        if config.debug:
            print(req)

        memo = ProgressMemo(
            subject_name=req.subject.name,
            subject_id=str(req.subject.id),
            subject_type_id=str(req.subject.type),
            eps_total=str(req.subject.eps_total) if req.subject.eps_total else "??",
            vols_total=str(req.subject.vols_total) if req.subject.vols_total else "??",
            eps_update=req.eps_update,
            vols_update=req.vols_update,
        )

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
                    cat=TimelineCat.Progress,
                    type=tlType,
                    batch=0,
                    related=str(req.subject.id),
                )
            )
            session.commit()

        return SubjectProgressResponse(ok=True)
