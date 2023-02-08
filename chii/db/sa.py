from typing import Callable

import sqlalchemy.orm
from sqlalchemy import (
    CHAR,
    Text,
    Column,
    String,
    DateTime,
    or_,
    and_,
    func,
    join,
    text,
    delete,
    select,
    update,
    create_engine,
)
from sqlalchemy.orm import joinedload, selectinload, sessionmaker, subqueryload
from sqlalchemy.dialects.mysql import insert

from chii.config import config

count = func.count

__all__ = [
    "CHAR",
    "selectinload",
    "joinedload",
    "Text",
    "Column",
    "subqueryload",
    "String",
    "DateTime",
    "func",
    "join",
    "text",
    "select",
    "update",
    "insert",
    "and_",
    "func",
    "count",
    "or_",
    "get",
    "delete",
    "sync_session_maker",
]


def get(T, *where, order=None):
    s = select(T).where(*where).limit(1)
    if order is not None:
        return s.order_by(order)
    return s


def sync_session_maker() -> Callable[[], sqlalchemy.orm.Session]:
    engine = create_engine(
        config.MYSQL_SYNC_DSN,
        pool_recycle=14400,
        pool_size=10,
        max_overflow=20,
        echo=config.debug,
    )
    return sessionmaker(engine)
