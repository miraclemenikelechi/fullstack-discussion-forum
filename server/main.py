from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from threads.route import router as threads_router
from authentication.route import router as authentication_router
from core.config import appConfig


app = FastAPI()
app.include_router(router=authentication_router, prefix=f"{appConfig.CURRENT_API_URL}")
app.include_router(router=threads_router, prefix=f"{appConfig.CURRENT_API_URL}")


@app.get("/")
async def root() -> None:
    return RedirectResponse("/docs")
