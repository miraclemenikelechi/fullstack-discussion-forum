from fastapi import APIRouter

from core.depedencies import DATABASE_SESSION_DEPENDENCY
from threads.controller import all_threads_from_db, create_a_new_thread
from utils.response import ResponseAPI

from .model import ThreadCreate, AllThreadsResponse

router = APIRouter(prefix="/threads", tags=["thread"])


@router.get(path="/", response_model=AllThreadsResponse)
async def get_all_threads(session: DATABASE_SESSION_DEPENDENCY):  # type: ignore
    try:
        request = await all_threads_from_db(db_access=session)

        if request is not None:
            return ResponseAPI(
                message="all threads",
                data=request,
                status_code=200,
                success=True,
            ).response()

    except Exception as error:
        return ResponseAPI(
            status_code=500,
            message=f"error getting all threads: {error}",
            success=False,
        ).response()


@router.post("/")
async def create_thread(data: ThreadCreate, session: DATABASE_SESSION_DEPENDENCY):  # type: ignore
    try:
        request = await create_a_new_thread(
            data_to_create_in_db=data, db_access=session
        )

        if request is not None:
            return ResponseAPI(
                message=f"thread `{request["id"]}` by user `{request["author"]}` has been created!",
                data=request,
                status_code=201,
                success=True,
            )

    except Exception as error:
        return ResponseAPI(
            status_code=500,
            message=f"error getting all threads: {error}",
            success=False,
        ).response()


@router.get("/{thread_id}")
async def get_thread(thread_id: str):
    return f"get {thread_id}"


@router.patch("/{thread_id}")
async def edit_thread(thread_id: str):
    pass


@router.delete("/{thread_id}")
async def delete_thread(thread_id: str):
    pass


@router.get("/{thread_id}/comments")
async def get_thread_comments(comment_id: str):
    pass


@router.post("/{thread_id}/comments")
async def create_thread_comment(comment_id: str):
    pass


@router.delete("/{thread_id}/comments/{comment_id}")
async def delete_thread_comment(comment_id: str):
    pass


@router.get("/{thread_id}/comments/{comment_id}/replies")
async def get_comment_reply():
    pass


@router.post("/{thread_id}/comments/{comment_id}/replies")
async def create_comment_reply():
    pass


@router.delete("/{thread_id}/comments/{comment_id}/replies/{reply_id}")
async def delete_comment_reply():
    pass
