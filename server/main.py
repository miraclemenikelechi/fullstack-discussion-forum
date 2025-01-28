from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from core.database import create_db_and_tables
from threads.route import router as threads_router
from authentication.route import router as authentication_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
# app.include_router(threads_router)
app.include_router(authentication_router)


@app.get("/")
async def root() -> None:
    return RedirectResponse("/docs")
