from fastapi import APIRouter

from core.depedencies import DATABASE_SESSION_DEPENDENCY
from utils.response import ResponseAPI, ResponseDataModel, ResponseErrorModel

from ..controllers.thread_get_all import get_all

router = APIRouter()


@router.get(
    path="/",
    status_code=200,
    responses={
        200: {"model": ResponseDataModel},
        500: {"model": ResponseErrorModel},
    },
)
async def get_all_threads(session: DATABASE_SESSION_DEPENDENCY):  # type: ignore
    try:
        request = await get_all(db_access=session)

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
    pass
