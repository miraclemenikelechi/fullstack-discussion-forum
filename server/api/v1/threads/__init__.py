from fastapi import APIRouter

#
from .routes.comment_create import router as create_thread_comment
from .routes.comment_get_all import router as get_all_thread_comments

#
from .routes.thread_create import router as create_thread
from .routes.thread_delete import router as delete_thread
from .routes.thread_edit import router as edit_thread
from .routes.thread_get import router as get_thread
from .routes.thread_get_all import router as get_all_thread

router = APIRouter(prefix="/threads", tags=["threads"])

# register routes under `/threads`
router.include_router(create_thread)
router.include_router(delete_thread)
router.include_router(edit_thread)
router.include_router(get_all_thread)
router.include_router(get_thread)

# register routes under `/threads/comments`
router.include_router(get_all_thread_comments)
router.include_router(create_thread_comment)
