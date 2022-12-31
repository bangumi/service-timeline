from typing import Dict

import phpserialize as php
from grpc import RpcContext
from loguru import logger
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from api.v1 import timeline_pb2_grpc
from chii.db import sa
from chii.compat import phpseralize
from chii.config import config
from chii.timeline import (
    SubjectMemo,
    TimelineCat,
    ProgressMemo,
    SubjectImage,
    subjectTypeMap,
)
from chii.db.tables import ChiiTimeline
from api.v1.timeline_pb2 import (
    HelloRequest,
    HelloResponse,
    EpisodeCollectRequest,
    SubjectCollectRequest,
    EpisodeCollectResponse,
    SubjectCollectResponse,
    SubjectProgressRequest,
    SubjectProgressResponse,
)


class TimeLineService(timeline_pb2_grpc.TimeLineServiceServicer):
    def __init__(self):
        self.SessionMaker = sa.sync_session_maker()

    def Hello(self, request: HelloRequest, context) -> HelloResponse:
        print(f"{config.node_id} rpc hello {request.name}")
        return HelloResponse(message=f"{config.node_id}: hello {request.name}")

    def SubjectCollect(
        self, request: SubjectCollectRequest, context: RpcContext
    ) -> SubjectCollectResponse:
        tlType = subjectTypeMap[request.subject.type][request.collection]
        if config.debug:
            print(request)
        logger.info(f"expected timeline {tlType}")
        with self.SessionMaker() as session:
            with session.begin():
                tl: ChiiTimeline = session.scalar(
                    sa.get(
                        ChiiTimeline,
                        ChiiTimeline.uid == request.user_id,
                        order=ChiiTimeline.id.desc(),
                    )
                )

                if tl:
                    logger.info("find previous timeline, merging")
                    if tl.cat == TimelineCat.Subject and tl.type == tlType:
                        self.merge_previous_timeline(session, tl, request)
                        return SubjectCollectResponse(ok=True)

                logger.info(
                    "missing previous timeline or timeline type mismatch, create a new timeline"
                )
                self.create_subject_collection_timeline(session, request, tlType)

        return SubjectCollectResponse(ok=True)

    def merge_previous_timeline(
        self, session: Session, tl: ChiiTimeline, req: SubjectCollectRequest
    ):
        if tl.batch:
            memo = parse_obj_as(
                Dict[int, SubjectMemo], phpseralize.loads(tl.memo.encode())
            )
        else:
            m = parse_obj_as(SubjectMemo, phpseralize.loads(tl.memo.encode()))
            if int(m.subject_id) == req.subject.id:
                # save request called twice, just ignore
                return
            memo = {int(m.subject_id): m}

        memo[req.subject.id] = SubjectMemo(
            subject_id=str(req.subject.id),
            subject_type_id=str(req.subject.type),
            subject_name_cn=req.subject.name,
            subject_series=req.subject.series,
            subject_name=req.subject.name_cn,
            collect_comment=req.comment,
            collect_rate=req.rate,
        )

        if tl.batch:
            img = parse_obj_as(
                Dict[int, SubjectImage], phpseralize.loads(tl.img.encode())
            )
        else:
            i = parse_obj_as(SubjectImage, phpseralize.loads(tl.img.encode()))
            img = {int(i.subject_id): i}

        img[req.subject.id] = SubjectImage(
            subject_id=str(req.subject.id), images=req.subject.image
        )

        tl.batch = 1
        tl.memo = php.serialize({key: value.dict() for key, value in memo.items()})
        tl.img = php.serialize({key: value.dict() for key, value in img.items()})

        session.add(tl)

    def create_subject_collection_timeline(
        self, session: Session, req: SubjectCollectRequest, type: int
    ):
        memo = SubjectMemo(
            subject_id=str(req.subject.id),
            subject_type_id=str(req.subject.type),
            subject_name_cn=req.subject.name,
            subject_series=req.subject.series,
            subject_name=req.subject.name_cn,
            collect_comment=req.comment,
            collect_rate=req.rate,
        )

        img = SubjectImage(subject_id=str(req.subject.id), images=req.subject.image)

        session.add(
            ChiiTimeline(
                cat=TimelineCat.Subject,
                type=type,
                uid=req.user_id,
                memo=php.serialize(memo.dict()),
                img=php.serialize(img.dict()),
                batch=0,
                related=str(req.subject.id),
            )
        )

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

        tlType = 0
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

        logger.info(f"expected timeline {tlType}")
        with self.SessionMaker() as session:
            tl: ChiiTimeline = session.scalar(
                sa.get(
                    ChiiTimeline,
                    ChiiTimeline.uid == req.user_id,
                    order=ChiiTimeline.id.desc(),
                )
            )

            with session.begin():
                if tl:
                    logger.info("find previous timeline, updating")
                    if (
                        tl.cat == TimelineCat.Progress
                        and tl.type == tlType
                        and tl.batch == 0
                        and tl.related == str(req.subject.id)
                    ):
                        tl.memo = php.serialize(memo)
                        session.add(tl)
                        return EpisodeCollectResponse(ok=True)

                session.add(
                    ChiiTimeline(
                        uid=req.user_id,
                        memo=php.serialize(memo.dict()),
                        img=php.serialize(img.dict()),
                        cat=TimelineCat.Progress,
                        type=tlType,
                        batch=0,
                        related=str(req.subject.id),
                    )
                )

        return EpisodeCollectResponse(ok=True)

    def SubjectProgress(
        self, req: SubjectProgressRequest, context
    ) -> SubjectProgressResponse:
        ProgressMemo(
            subject_name=req.subject.name,
            subject_id=str(req.subject.id),
            subject_type_id=str(req.subject.type),
            eps_total=str(req.subject.eps_total) if req.subject.eps_total else "??",
            vols_total=str(req.subject.vols_total) if req.subject.vols_total else "??",
            eps_update=req.eps_update,
            vols_update=req.vols_update,
        )

        tlType = 2

        img = SubjectImage(
            subject_id=str(req.subject.id),
            images=req.subject.image,
        )

        if config.debug:
            print(req)

        logger.info(f"expected timeline {tlType}")
        with self.SessionMaker() as session:
            tl: ChiiTimeline = session.scalar(
                sa.get(
                    ChiiTimeline,
                    ChiiTimeline.uid == req.user_id,
                    order=ChiiTimeline.id.desc(),
                )
            )

            with session.begin():
                if tl:
                    logger.info("find previous timeline, updating")
                    if (
                        tl.cat == TimelineCat.Progress
                        and tl.type == tlType
                        and tl.batch == 0
                        and tl.related == str(req.subject.id)
                    ):
                        tl.memo = php.serialize(memo)
                        session.add(tl)
                        return SubjectProgressResponse(ok=True)

                session.add(
                    ChiiTimeline(
                        uid=req.user_id,
                        memo=php.serialize(memo.dict()),
                        img=php.serialize(img.dict()),
                        cat=TimelineCat.Progress,
                        type=tlType,
                        batch=0,
                        related=str(req.subject.id),
                    )
                )

        return SubjectProgressResponse(ok=True)
