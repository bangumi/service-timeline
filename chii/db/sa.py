import time

from sqlalchemy import (
    CHAR,
    Column,
    Connection,
    DateTime,
    String,
    Text,
    and_,
    create_engine,
    delete,
    event,
    func,
    join,
    or_,
    select,
    text,
    update,
)
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import joinedload, selectinload, sessionmaker, subqueryload
from sslog import logger

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
        execution_options={"statement_timeout": config.MYSQL_STMT_TIMEOUT},
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
