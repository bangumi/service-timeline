from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from chii.db import sa
from chii.db.tables import Base

T = TypeVar("T", bound=Base)


async def count(db: AsyncSession, *where) -> int:
    query = sa.select(sa.func.count(1)).where(*where)  # type: ignore
    return int(await db.scalar(query))
