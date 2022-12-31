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
            if m.subject_id == req.subject.id:
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
        self, request: EpisodeCollectRequest, context
    ) -> EpisodeCollectResponse:

        ProgressMemo(
            ep_id=request.last.id,
            subject_name=request.subject.name,
            ep_name=request.last.name,
            subject_id=str(request.subject.id),
            subject_type_id=str(request.subject.type),
            ep_sort=request.last.sort,
        )

        return EpisodeCollectResponse(ok=True)

    def SubjectProgress(
        self, request: SubjectProgressRequest, context
    ) -> SubjectProgressResponse:
        ProgressMemo(
            subject_name=request.subject.name,
            subject_id=str(request.subject.id),
            subject_type_id=str(request.subject.type),
            eps_total=str(request.subject.eps_total)
            if request.subject.eps_total
            else "??",
            vols_total=str(request.subject.vols_total)
            if request.subject.vols_total
            else "??",
            eps_update=request.eps_update,
            vols_update=request.vols_update,
        )

        return SubjectProgressResponse(ok=True)
