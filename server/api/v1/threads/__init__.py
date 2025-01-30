from fastapi import APIRouter

from .routes.thread_get_all import router as thread


router = APIRouter(prefix="/threads", tags=["thread"])

router.include_router(thread)
