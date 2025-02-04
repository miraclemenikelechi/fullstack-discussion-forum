from fastapi import APIRouter

# comments' routes
from .routes.comment_create import router as create_a_comment_in_a_thread
from .routes.comment_delete import router as delete_a_comment_from_a_thread
from .routes.comment_get_all import router as get_all_comments_from_thread

# replies' routes
from .routes.reply_create import router as create_reply_to_comment
from .routes.reply_get_all import router as get_replies_to_a_comment

# threads' routes
from .routes.thread_create import router as create_a_new_thread
from .routes.thread_delete import router as delete_a_thread
from .routes.thread_edit import router as edit_a_thread
from .routes.thread_get import router as get_a_thread
from .routes.thread_get_all import router as get_all_threads

# fastapi route
router = APIRouter(prefix="/threads", tags=["threads"])


# register routes under `/{thread}s`
router.include_router(create_a_new_thread)
router.include_router(delete_a_thread)
router.include_router(edit_a_thread)
router.include_router(get_a_thread)
router.include_router(get_all_threads)


# register routes under `/{thread}/{comment}s`
router.include_router(create_a_comment_in_a_thread)
router.include_router(delete_a_comment_from_a_thread)
router.include_router(get_all_comments_from_thread)


# register routes under `/{thread}/{comment}/{reply}s`
router.include_router(create_reply_to_comment)
router.include_router(get_replies_to_a_comment)
