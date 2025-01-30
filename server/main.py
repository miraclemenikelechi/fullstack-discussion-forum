from fastapi import FastAPI
from fastapi.responses import RedirectResponse

# from chains.route.chain import chain_routes, ChainRoutes
# from threads.routes import router as threads_router
# from authentication.route import router as authentication_router
from core.config import appConfig


from api.v1.authentication.routes.sign_in import router as authentication_router


app = FastAPI()
app.include_router(router=authentication_router, prefix=f"{appConfig.CURRENT_API_URL}")
# # app.include_router(router=threads_router, prefix=f"{appConfig.CURRENT_API_URL}")
# app.include_router(ChainRoutes().router)


@app.get("/")
async def root() -> None:
    return RedirectResponse("/docs")
