from fastapi.exceptions import HTTPException

from core.depedencies import DATABASE_SESSION_DEPENDENCY
from utils.response import ResponseAPI, ResponseDataModel

from .. import router
from ..controllers import sign_in_a_user
from ..models.signin import UserSignIn


# from ..controllers.sign_in_a_user import sign_in_a_user


@router.post(path="/login", status_code=200)
async def signin(data: UserSignIn, session: DATABASE_SESSION_DEPENDENCY):  # type: ignore
    try:
        request = await sign_in_a_user(user_to_sign_in=data, db_access=session)

        if request is not None:
            return ResponseAPI(
                message="Log in success.",
                data=request,
                status_code=200,
                success=True,
            ).response()

    except HTTPException as error:
        raise error

    except Exception as error:
        return ResponseAPI(
            message=f"An error occurred: {error}",
            status_code=500,
            success=False,
        ).response()
