import logging.config
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
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import joinedload, selectinload, sessionmaker, subqueryload
from sslog import logger

from chii.config import config

count = func.count

__all__ = [
    "CHAR",
    "Column",
    "DateTime",
    "String",
    "Text",
    "and_",
    "count",
    "delete",
    "func",
    "func",
    "get",
    "insert",
    "join",
    "joinedload",
    "or_",
    "select",
    "selectinload",
    "subqueryload",
    "sync_session_maker",
    "text",
    "update",
]


def get(T, *where, order=None):
    s = select(T).where(*where).limit(1)
    if order is not None:
        return s.order_by(order)
    return s


if config.debug:
    # redirect echo logger to sslog
    logging.config.dictConfig(
        {
            "version": 1,
            "handlers": {
                "sslog": {
                    "class": "sslog.InterceptHandler",
                    "level": "DEBUG",
                }
            },
            "loggers": {
                "": {"level": "INFO", "handlers": ["sslog"]},
                "sqlalchemy.engine.Engine": {
                    "level": "INFO",
                    "handlers": ["sslog"],
                    "propagate": False,
                },
            },
        }
    )


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


def async_session_maker():
    engine = create_async_engine(
        config.MYSQL_ASYNC_DSN(),
        pool_recycle=14400,
        pool_size=10,
        max_overflow=20,
        echo=config.debug,
        execution_options={"statement_timeout": config.MYSQL_STMT_TIMEOUT},
    )

    return async_sessionmaker(engine)


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
