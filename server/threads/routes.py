from fastapi import APIRouter, HTTPException

from core.depedencies import DATABASE_SESSION_DEPENDENCY, CURRENT_USER_DEPENDENCY
from threads.controllers import (
    all_threads_from_db,
    create_a_new_thread,
    create_a_reply_to_comment_in_a_thread,
    create_comment_in_a_thread,
    delete_a_reply_from_comment_in_a_thread,
    delete_a_thread,
    delete_comment_from_a_thread,
    get_a_thread,
    get_all_comments_from_a_thread,
    get_all_replies_from_comment_in_a_thread,
    update_a_thread,
)
from utils.response import ResponseAPI, ResponseApiModel, ResponseDataModel

from .model import CommentCreate, ThreadCreate, ThreadUpdate

router = APIRouter(prefix="/threads", tags=["thread"])


@router.get(path="/", status_code=200, response_model=ResponseDataModel)
async def get_all_threads(session: DATABASE_SESSION_DEPENDENCY):  # type: ignore
    try:
        request = await all_threads_from_db(db_access=session)

        if request is not None:
            return ResponseAPI(
                data=request,
                message="all threads",
                status_code=200,
                success=True,
            ).response()

    except Exception as error:
        return ResponseAPI(
            message=f"An error occured: {error}",
            status_code=500,
            success=False,
        ).response()


@router.post(path="/", status_code=201, response_model=ResponseApiModel)
async def create_thread(
    data: ThreadCreate,
    session: DATABASE_SESSION_DEPENDENCY,  # type: ignore
    current_user: CURRENT_USER_DEPENDENCY,  # type: ignore
):
    try:
        request = await create_a_new_thread(
            data_to_create_in_db=data, db_access=session, thread_author=current_user
        )

        if request is not None:
            return ResponseAPI(
                data=request,
                message=f"thread `{request['id']}` by user `{request['author_username']}` has been created!",
                status_code=201,
                success=True,
            )

    except Exception as error:
        return ResponseAPI(
            message=f"An error occured: {error}",
            status_code=500,
            success=False,
        ).response()


@router.get(path="/{thread_id}", status_code=200, response_model=ResponseApiModel)
async def get_thread(thread_id: str, session: DATABASE_SESSION_DEPENDENCY):  # type: ignore
    try:
        request = await get_a_thread(data_to_fetch_in_db=thread_id, db_access=session)

        if request is not None:
            return ResponseAPI(
                data=request,
                message=f"thread `{request['id']}` by `{request['author']}`",
                status_code=200,
                success=True,
            )

    except HTTPException as error:
        raise error

    except Exception as error:
        return ResponseAPI(
            message=f"An error occured: {error}",
            status_code=500,
            success=False,
        ).response()


@router.patch(path="/{thread_id}", status_code=202, response_model=ResponseDataModel)
async def edit_thread(
    thread_id: str,
    thread_update: ThreadUpdate,
    session: DATABASE_SESSION_DEPENDENCY,  # type: ignore
    current_user: CURRENT_USER_DEPENDENCY,  # type: ignore
):
    try:
        request = await update_a_thread(
            data_to_fetch_in_db=thread_id,
            data_to_update_in_db=thread_update,
            db_access=session,
            current_user=current_user,
        )

        if request is not None:
            return ResponseAPI(
                data=request,
                message=f"thread `{request['id']}` has been updated.",
                status_code=202,
                success=True,
            ).response()

    except HTTPException as error:
        raise error

    except Exception as error:
        return ResponseAPI(
            message=f"An error occured: {error}",
            status_code=500,
            success=False,
        ).response()


@router.delete(path="/{thread_id}", status_code=200, response_model=ResponseDataModel)
async def delete_thread(
    thread_id: str,
    session: DATABASE_SESSION_DEPENDENCY,  # type: ignore
    current_user: CURRENT_USER_DEPENDENCY,  # type: ignore
):
    try:
        request = await delete_a_thread(
            data_to_fetch_in_db=thread_id, db_access=session, current_user=current_user
        )

        if request is not None:
            return ResponseAPI(
                message=f"thread `{request['id']}` has been deleted.",
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


@router.get(
    path="/{thread_id}/comments", status_code=200, response_model=ResponseDataModel
)
async def get_thread_comments(thread_id: str, session: DATABASE_SESSION_DEPENDENCY):  # type: ignore
    try:
        request = await get_all_comments_from_a_thread(
            data_to_fetch_in_db=thread_id, db_access=session
        )

        if request is not None:
            return ResponseAPI(
                data=request["comments"],
                message=f"all comments from thread `{request['id']}`.",
                status_code=200,
                success=True,
            ).response()

    except HTTPException as error:
        raise error

    except Exception as error:
        return ResponseAPI(
            message=f"An error occured: {error}",
            status_code=500,
            success=False,
        ).response()


@router.post(
    path="/{thread_id}/comments", status_code=201, response_model=ResponseDataModel
)
async def create_thread_comment(
    thread_id: str,
    comment_create: CommentCreate,
    session: DATABASE_SESSION_DEPENDENCY,  # type: ignore
):
    try:
        request = await create_comment_in_a_thread(
            data_to_fetch_in_db=thread_id,
            data_to_update_in_db=comment_create,
            db_access=session,
        )

        if request is not None:
            return ResponseAPI(
                data=request,
                message=f"comment `{request['id']}` created in response to thread `{request['thread_id']}`",
                status_code=201,
                success=True,
            ).response()

    except HTTPException as error:
        raise error

    except Exception as error:
        return ResponseAPI(
            message=f"An error occured: {error}",
            status_code=500,
            success=False,
        ).response()


@router.delete(
    path="/{thread_id}/comments/{comment_id}",
    status_code=200,
    response_model=ResponseDataModel,
)
async def delete_thread_comment(
    thread_id: str,
    comment_id: str,
    session: DATABASE_SESSION_DEPENDENCY,  # type: ignore
):
    try:
        request = await delete_comment_from_a_thread(
            data_to_fetch_in_db=thread_id,
            data_to_transact_with_in_db=comment_id,
            db_access=session,
        )

        if request is not None:
            return ResponseAPI(
                message=f"comment `{request['id']}` has been deleted from thread `{request['thread_id']}`",
                status_code=200,
                success=True,
            ).response()

    except HTTPException as error:
        raise error

    except Exception as error:
        return ResponseAPI(
            message=f"An error occured: {error}",
            status_code=500,
            success=False,
        ).response()


@router.get(
    path="/{thread_id}/comments/{comment_id}/replies",
    status_code=200,
    response_model=ResponseDataModel,
)
async def get_comment_replies(
    thread_id: str,
    comment_id: str,
    session: DATABASE_SESSION_DEPENDENCY,  # type: ignore
):
    try:
        request = await get_all_replies_from_comment_in_a_thread(
            data_to_fetch_in_db=thread_id,
            data_to_transact_with_in_db=comment_id,
            db_access=session,
        )

        if request is not None:
            return ResponseAPI(
                data=request["replies"],
                message=f"comment `{request['id']}` replies on thread `{request['thread_id']}`",
                status_code=200,
                success=True,
            ).response()

    except HTTPException as error:
        raise error

    except Exception as error:
        return ResponseAPI(
            message=f"An error occured: {error}",
            status_code=500,
            success=False,
        ).response()


@router.post(
    path="/{thread_id}/comments/{comment_id}/replies",
    status_code=201,
    response_model=ResponseDataModel,
)
async def create_comment_reply(
    thread_id: str,
    comment_id: str,
    reply_create: CommentCreate,
    session: DATABASE_SESSION_DEPENDENCY,  # type: ignore
):
    try:
        request = await create_a_reply_to_comment_in_a_thread(
            data_to_update_in_db=reply_create,
            data_to_fetch_in_db=thread_id,
            data_to_transact_with_in_db=comment_id,
            db_access=session,
        )

        if request is not None:
            return ResponseAPI(
                data=request,
                message=f"reply `{request['id']}` created in response to comment `{request['comment_id']}`",
                status_code=201,
                success=True,
            ).response()

    except HTTPException as error:
        raise error

    except Exception as error:
        return ResponseAPI(
            message=f"An error occured: {error}",
            status_code=500,
            success=False,
        ).response()


@router.delete("/{thread_id}/comments/{comment_id}/replies/{reply_id}")
async def delete_comment_reply(
    thread_id: str,
    comment_id: str,
    reply_id: str,
    session: DATABASE_SESSION_DEPENDENCY,  # type: ignore
):
    try:
        request = await delete_a_reply_from_comment_in_a_thread(
            data_to_fetch_in_db=comment_id,
            data_to_transact_with_in_db=reply_id,
            db_access=session,
        )

        if request is not None:
            return ResponseAPI(
                message=f"reply `{request['id']}` to comment `{request['comment_id']}` has been deleted from thread `{thread_id}`",
                status_code=200,
                success=True,
            ).response()

    except HTTPException as error:
        raise error

    except Exception as error:
        return ResponseAPI(
            message=f"An error occured: {error}",
            status_code=500,
            success=False,
        ).response()
