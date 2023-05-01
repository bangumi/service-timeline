from typing import Dict, List, Union

from loguru import logger
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from chii import timeline
from chii.db import sa
from chii.compat import phpseralize
from chii.db.tables import ChiiTimeline

step = 100


@logger.catch()
def main():
    SessionMaker = sa.sync_session_maker()
    with SessionMaker() as session:
        max_tml_id = get_max_timeline_id(session)
        last_id = 0

        while True:
            tls: List[ChiiTimeline] = session.scalars(
                sa.select(ChiiTimeline)
                .where(ChiiTimeline.tml_id >= last_id)
                .limit(step)
                .order_by(ChiiTimeline.tml_id.asc())
            )

            for tl in tls:
                last_id = tl.tml_id
                timeline.parseTimeLine(tl)
                # if tl.tml_memo:

                if tl.tml_img:
                    try:
                        img = phpseralize.loads(tl.img.encode())
                    except Exception as e:
                        print("image", e)
                        continue

                    parse_obj_as(Union[Dict[int, timeline.Image], timeline.Image], img)

            if last_id >= max_tml_id:
                break


def get_max_timeline_id(session: Session):
    return session.scalar(
        sa.select(ChiiTimeline.tml_id).order_by(ChiiTimeline.tml_id.desc()).limit(1)
    )


if __name__ == "__main__":
    print("start")
    main()
