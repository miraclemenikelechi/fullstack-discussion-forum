from fastapi import APIRouter

from core.depedencies import DATABASE_SESSION_DEPENDENCY
from threads.controller import (
    all_threads_from_db,
    create_a_new_thread,
    get_a_thread,
    update_a_thread,
)
from utils.response import ResponseAPI, ResponseApiModel, ResponseDataModel

from .model import ThreadCreate, ThreadUpdate

router = APIRouter(prefix="/threads", tags=["thread"])


@router.get(path="/", status_code=200, response_model=ResponseDataModel)
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
            message=f"error getting all threads <<==>> {error}",
            success=False,
        ).response()


@router.post("/", status_code=201, response_model=ResponseApiModel)
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
            message=f"error creating your thread at this time <<==>> {error}",
            success=False,
        ).response()


@router.get("/{thread_id}", status_code=200, response_model=ResponseApiModel)
async def get_thread(thread_id: str, session: DATABASE_SESSION_DEPENDENCY):  # type: ignore
    try:
        request = await get_a_thread(data_to_fetch_in_db=thread_id, db_access=session)

        if request is not None:
            return ResponseAPI(
                message=f"thread `{request["id"]}` by `{request["author"]}`",
                data=request,
                status_code=200,
                success=True,
            )

    except Exception as error:
        return ResponseAPI(
            status_code=500,
            message=f"cannot get thread `{thread_id}` <<==>> {error}",
            success=False,
        ).response()


@router.patch("/{thread_id}")
async def edit_thread(
    thread_id: str,
    thread_update: ThreadUpdate,
    session: DATABASE_SESSION_DEPENDENCY,  # type: ignore
):
    try:
        request = await update_a_thread(
            data_to_fetch_in_db=thread_id,
            data_to_update_in_db=thread_update,
            db_access=session,
        )

        if request is not None:
            return ResponseAPI(
                message=f"thread `{request["id"]}` has been updated.",
                data=request,
                status_code=200,
                success=True,
            ).response()

    except ValueError as error:
        return ResponseAPI(
            status_code=404,
            message=f"{error}",
            success=False,
        ).response()

    except Exception as error:
        return ResponseAPI(
            status_code=500,
            message=f"{error}",
            success=False,
        ).response()


@router.delete("/{thread_id}")
async def delete_thread(thread_id: str):
    try:
        pass

    except Exception as error:
        return ResponseAPI(
            status_code=500,
            message=f"{error}",
            success=False,
        ).response()


@router.get("/{thread_id}/comments")
async def get_thread_comments(comment_id: str):
    try:
        pass

    except Exception as error:
        return ResponseAPI(
            status_code=500,
            message=f"{error}",
            success=False,
        ).response()


@router.post("/{thread_id}/comments")
async def create_thread_comment(comment_id: str):
    try:
        pass

    except Exception as error:
        return ResponseAPI(
            status_code=500,
            message=f"{error}",
            success=False,
        ).response()


@router.delete("/{thread_id}/comments/{comment_id}")
async def delete_thread_comment(comment_id: str):
    try:
        pass

    except Exception as error:
        return ResponseAPI(
            status_code=500,
            message=f"{error}",
            success=False,
        ).response()


@router.get("/{thread_id}/comments/{comment_id}/replies")
async def get_comment_reply():
    try:
        pass

    except Exception as error:
        return ResponseAPI(
            status_code=500,
            message=f"{error}",
            success=False,
        ).response()


@router.post("/{thread_id}/comments/{comment_id}/replies")
async def create_comment_reply():
    try:
        pass

    except Exception as error:
        return ResponseAPI(
            status_code=500,
            message=f"{error}",
            success=False,
        ).response()


@router.delete("/{thread_id}/comments/{comment_id}/replies/{reply_id}")
async def delete_comment_reply():
    try:
        pass

    except Exception as error:
        return ResponseAPI(
            status_code=500,
            message=f"{error}",
            success=False,
        ).response()
