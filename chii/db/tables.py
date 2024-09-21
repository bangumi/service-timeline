import datetime
import html
import time
from dataclasses import dataclass, field
from typing import cast

from sqlalchemy import Column, String, text, types
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
    memo: bytes = field(
        default=b"", metadata={"sa": Column("tml_memo", MEDIUMTEXT, nullable=False)}
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


class HTMLEscapedString(types.TypeDecorator):
    impl = String

    cache_ok = True

    def process_bind_param(self, value, dialect):
        """python value to db value"""
        return html.escape(value)

    def process_result_value(self, value, dialect):
        """db value to python value"""
        return html.unescape(value)


@reg.mapped
@dataclass(kw_only=True)
class ChiiSubject:
    __tablename__ = "chii_subjects"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(
        metadata={"sa": Column("subject_id", MEDIUMINT(8), primary_key=True)}
    )
    type_id: int = field(
        metadata={
            "sa": Column("subject_type_id", SMALLINT(6), server_default=text("'0'"))
        }
    )
    name: str = field(metadata={"sa": Column("subject_name", HTMLEscapedString(80))})
    name_cn: str = field(
        metadata={"sa": Column("subject_name_cn", HTMLEscapedString(80))}
    )
    user_id: str = field(
        metadata={"sa": Column("subject_uid", String(20), comment="isbn / imdb")}
    )
    creator: int = field(metadata={"sa": Column("subject_creator", MEDIUMINT(8))})
    created_at: int = field(
        metadata={
            "sa": Column("subject_dateline", INTEGER(10), server_default=text("'0'"))
        }
    )
    image: str = field(metadata={"sa": Column("subject_image", String(255))})
    platform: int = field(
        metadata={
            "sa": Column("subject_platform", SMALLINT(6), server_default=text("'0'"))
        }
    )
    infobox: str = field(metadata={"sa": Column("field_infobox", MEDIUMTEXT)})
    summary: str = field(
        metadata={"sa": Column("field_summary", MEDIUMTEXT, comment="summary")}
    )
    author_summary: str = field(
        metadata={"sa": Column("field_5", MEDIUMTEXT, comment="author summary")}
    )
    volumes: int = field(
        metadata={
            "sa": Column(
                "field_volumes",
                MEDIUMINT(8),
                server_default=text("'0'"),
                comment="卷数",
            )
        }
    )
    eps: int = field(
        metadata={"sa": Column("field_eps", MEDIUMINT(8), server_default=text("'0'"))}
    )
    wish: int = field(
        metadata={
            "sa": Column("subject_wish", MEDIUMINT(8), server_default=text("'0'"))
        }
    )
    collect: int = field(
        metadata={
            "sa": Column("subject_collect", MEDIUMINT(8), server_default=text("'0'"))
        }
    )
    doing: int = field(
        metadata={
            "sa": Column("subject_doing", MEDIUMINT(8), server_default=text("'0'"))
        }
    )
    on_hold: int = field(
        metadata={
            "sa": Column(
                "subject_on_hold",
                MEDIUMINT(8),
                server_default=text("'0'"),
                comment="搁置人数",
            )
        }
    )
    dropped: int = field(
        metadata={
            "sa": Column(
                "subject_dropped",
                MEDIUMINT(8),
                server_default=text("'0'"),
                comment="抛弃人数",
            )
        }
    )
    series: int = field(
        metadata={
            "sa": Column("subject_series", TINYINT(1), server_default=text("'0'"))
        }
    )
    series_entry: int = field(
        metadata={
            "sa": Column(
                "subject_series_entry", MEDIUMINT(8), server_default=text("'0'")
            )
        }
    )
    idx_cn: str = field(metadata={"sa": Column("subject_idx_cn", String(1))})
    airtime: int = field(metadata={"sa": Column("subject_airtime", TINYINT(1))})
    nsfw: int = field(metadata={"sa": Column("subject_nsfw", TINYINT(1))})
    ban: int = field(
        metadata={"sa": Column("subject_ban", TINYINT(1), server_default=text("'0'"))}
    )
