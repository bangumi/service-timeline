from pathlib import Path
from typing import Any, Iterator

from ariadne import ObjectType, QueryType, gql, make_executable_schema
from ariadne.asgi import GraphQL
from sqlalchemy import select
from starlette.applications import Starlette
from starlette.routing import Mount

from chii.compat import phpseralize
from chii.const import CollectionType
from chii.db import sa
from chii.db.tables import ChiiTimeline, ChiiTimeline_column_cat, ChiiTimeline_column_id
from chii.timeline import TimelineCat
from gql.model import CollectTimeline
from gql.rules import depth_limit_validator

# Define types using Schema Definition Language (https://graphql.org/learn/schema/)
# Wrapping string in gql function provides validation and better error traceback
type_defs = gql(
    Path(__file__, "..", "schema.graphql").resolve().read_text(encoding="utf8")
)

CreateSession = sa.async_session_maker()

# Map resolver functions to Query fields using QueryType
gql_query = QueryType()


# Resolvers are simple python functions
@gql_query.field("timeline_collection")
async def timeline_collection(*_: Any) -> list[CollectTimeline]:
    async with CreateSession() as session:
        rows: Iterator[ChiiTimeline] = await session.scalars(
            select(ChiiTimeline)
            .where(ChiiTimeline_column_cat == TimelineCat.Subject)
            .order_by(ChiiTimeline_column_id.desc())
            .limit(10)
        )

        result = []
        for row in rows:
            meme = phpseralize.loads(row.memo.encode())
            if not row.batch:
                result.append(
                    CollectTimeline(
                        id=row.id,
                        action=CollectionType.wish,
                        user_id=row.uid,
                        subject_id=[int(meme["subject_id"])],
                        created_at=row.created_at,
                    )
                )
            else:
                result.append(
                    CollectTimeline(
                        id=row.id,
                        action=CollectionType.wish,
                        user_id=row.uid,
                        subject_id=[int(x) for x in meme],
                        created_at=row.created_at,
                    )
                )

        return result


# Map resolver functions to custom type fields using ObjectType
gql_collect_timeline = ObjectType("CollectTimeline")

# Create executable GraphQL schema
schema = make_executable_schema(type_defs, gql_query, gql_collect_timeline)

app = Starlette(
    debug=True,
    routes=[
        Mount(
            "/graphql",
            GraphQL(
                schema,
                debug=True,
                validation_rules=[depth_limit_validator(max_depth=5)],
            ),
        ),
    ],
)
