from fastapi import APIRouter

from .routes.thread import router as thread


router = APIRouter(prefix="/threads", tags=["thread"])

router.include_router(thread)
