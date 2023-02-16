import time

from loguru import logger
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
    event,
    delete,
    select,
    update,
    create_engine,
)
from sqlalchemy.orm import joinedload, selectinload, sessionmaker, subqueryload
from sqlalchemy.engine import Engine
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


def sync_session_maker():
    engine = create_engine(
        config.MYSQL_SYNC_DSN,
        pool_recycle=14400,
        pool_size=10,
        max_overflow=20,
        echo=config.debug,
    )
    return sessionmaker(engine)


if config.SLOW_SQL_MS:
    duration = config.SLOW_SQL_MS * 1000000

    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        conn.info.setdefault("query_start_time", time.monotonic_ns())

    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        total = time.monotonic_ns() - conn.info["query_start_time"]
        print(total)
        if total > duration:
            logger.warning(
                "slow sql",
                statement=statement,
                parameters=parameters,
                duration_ns=total,
            )
