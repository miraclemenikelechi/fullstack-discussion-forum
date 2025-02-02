from fastapi import APIRouter

from .routes.thread_create import router as create_thread
from .routes.thread_edit import router as edit_thread
from .routes.thread_get import router as get_thread
from .routes.thread_get_all import router as get_all_thread

router = APIRouter(prefix="/threads", tags=["threads"])

# register routes under `/threads`
router.include_router(create_thread)
router.include_router(edit_thread)
router.include_router(get_all_thread)
router.include_router(get_thread)
