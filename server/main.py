from contextlib import asynccontextmanager

import strawberry
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from strawberry.fastapi import GraphQLRouter

from config.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


@strawberry.type
class Movie:
    title: str
    director: str


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


schema = strawberry.Schema(query=Query)

graphql_app = GraphQLRouter(schema)


app = FastAPI(lifespan=lifespan)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root() -> None:
    return RedirectResponse("/docs")
