from typing import Optional

from sqlalchemy import select

from api.v1.timeline_pb2 import HelloRequest
from chii.db import sa
from chii.db.const import CollectionType
from chii.db.tables import ChiiTimeline, ChiiTimeline_column_id, ChiiTimeline_column_uid
from chii.subject import SubjectType
from chii.timeline import SUBJECT_TYPE_MAP, TimelineCat
from rpc.timeline_service import TimeLineService


def test_Hello():
    assert (
        TimeLineService()
        .Hello(HelloRequest(name="nn"), None)
        .message.endswith("hello from nn")
    )


SessionMaker = sa.sync_session_maker()


def test_get() -> None:
    with SessionMaker.begin() as session:
        tl: Optional[ChiiTimeline] = session.scalar(
            select(ChiiTimeline)
            .where(ChiiTimeline_column_uid == 204)
            .order_by(ChiiTimeline_column_id.desc())
            .limit(1)
        )

        assert tl
        assert tl.uid == 204

        session.add(
            ChiiTimeline(
                uid=1,
                cat=TimelineCat.Wiki,
                type=SUBJECT_TYPE_MAP[SubjectType.anime][CollectionType.wish],
                batch=False,
            )
        )
