import datetime
import time
from dataclasses import dataclass, field
from typing import cast

from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import (
    CHAR,
    INTEGER,
    MEDIUMINT,
    MEDIUMTEXT,
    SMALLINT,
    TINYINT,
)
from sqlalchemy.orm import registry

reg: registry = registry()


@reg.mapped
@dataclass(kw_only=True)
class ChiiTimeline:
    __tablename__ = "chii_timeline"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(
        init=False, metadata={"sa": Column("tml_id", INTEGER(10), primary_key=True)}
    )
    uid: int = field(
        metadata={
            "sa": Column(
                "tml_uid",
                MEDIUMINT(8),
                nullable=False,
                index=True,
                server_default=text("'0'"),
            )
        }
    )
    cat: int = field(
        metadata={"sa": Column("tml_cat", SMALLINT(6), nullable=False, index=True)}
    )
    type: int = field(
        metadata={
            "sa": Column(
                "tml_type", SMALLINT(6), nullable=False, server_default=text("'0'")
            )
        }
    )
    related: str = field(
        default="0",
        metadata={
            "sa": Column(
                "tml_related",
                CHAR(255),
                nullable=False,
                server_default=text("'0'"),
                default=0,
            )
        },
    )
    memo: str = field(
        default="", metadata={"sa": Column("tml_memo", MEDIUMTEXT, nullable=False)}
    )
    img: str = field(
        default="",
        metadata={"sa": Column("tml_img", MEDIUMTEXT, nullable=False, default="")},
    )
    batch: int = field(
        metadata={"sa": Column("tml_batch", TINYINT(3), nullable=False, index=True)}
    )
    source: int = field(
        default=0,
        metadata={
            "sa": Column(
                "tml_source",
                TINYINT(3),
                nullable=False,
                server_default=text("'0'"),
                comment="更新来源",
                default=5,
            )
        },
    )
    replies: int = field(
        default=0,
        metadata={
            "sa": Column(
                "tml_replies", MEDIUMINT(8), nullable=False, comment="回复数", default=0
            )
        },
    )
    dateline: int = field(
        default_factory=lambda: int(time.time()),
        metadata={
            "sa": Column(
                "tml_dateline",
                INTEGER(10),
                nullable=False,
                server_default=text("'0'"),
                default=lambda: int(datetime.datetime.now().timestamp()),
            )
        },
    )


# type helper for ChiiTimeline.uid.desc()
ChiiTimeline_column_id: Column[int] = cast(Column[int], ChiiTimeline.id)
ChiiTimeline_column_uid: Column[int] = cast(Column[int], ChiiTimeline.uid)
