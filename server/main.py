from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from auth.login_route import router as authentication_router
from threads.route import router as threads_router


app = FastAPI()
app.include_router(authentication_router)
app.include_router(threads_router)


@app.get("/")
async def root() -> None:
    return RedirectResponse("/docs")
