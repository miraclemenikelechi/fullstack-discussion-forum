from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.v1.authentication import router as authentication_router
from api.v1.threads import router as threads_router
from core.config import appConfig

app = FastAPI()

# register routes
app.include_router(router=authentication_router, prefix=f"{appConfig.CURRENT_API_URL}")
app.include_router(router=threads_router, prefix=f"{appConfig.CURRENT_API_URL}")


@app.get("/")
async def root() -> None:
    return RedirectResponse("/docs")
