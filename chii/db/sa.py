import time

from loguru import logger
from sqlalchemy import (
    CHAR,
    Text,
    Column,
    String,
    DateTime,
    Connection,
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

    if config.SLOW_SQL_MS:
        event.listen(engine, "before_cursor_execute", before_cursor_execute)
        event.listen(engine, "after_cursor_execute", after_cursor_execute)

    return sessionmaker(engine)


def before_cursor_execute(
    conn: Connection, cursor, statement, parameters, context, executemany
):
    conn.info.setdefault("query_start_time", []).append(time.time())


def after_cursor_execute(
    conn: Connection, cursor, statement, parameters, context, executemany
):
    start = conn.info["query_start_time"].pop(-1)
    end = time.time()
    total = end - start
    if total * 1000 > config.SLOW_SQL_MS:
        logger.warning(
            "slow sql",
            statement=statement,
            parameters=parameters,
            duration_seconds=total,
            start=start,
            end=end,
        )
