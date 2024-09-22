from pathlib import Path

from ariadne import ObjectType, QueryType, gql, make_executable_schema
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.routing import Mount

from chii.const import CollectionType
from gql.model import CollectTimeline

# Define types using Schema Definition Language (https://graphql.org/learn/schema/)
# Wrapping string in gql function provides validation and better error traceback
type_defs = gql(
    Path(__file__, "..", "schema.graphql").resolve().read_text(encoding="utf8")
)

# Map resolver functions to Query fields using QueryType
query = QueryType()


# Resolvers are simple python functions
@query.field("timeline_collection")
async def timeline_collection(*_):
    return [
        CollectTimeline(
            action=CollectionType.wish, subject_name="test", subject_name_cn="test2"
        ),
    ]


# Map resolver functions to custom type fields using ObjectType
person = ObjectType("CollectTimeline")

# Create executable GraphQL schema
schema = make_executable_schema(type_defs, query, person)

app = Starlette(
    debug=True,
    routes=[
        Mount("/graphql", GraphQL(schema, debug=True)),
    ],
)
