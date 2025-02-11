from sqlmodel import Session

from api.v1.user.models.user import User
from utils.response import raiseHttpError

from ..models.login import UserLoginForm
from ..services.auth_by_id import authenticate_by_identifier
from ..services.create_access_token import create_access_token
from ..services.verify_password import verify_password


async def sign_in_a_user(
    user_to_sign_in: UserLoginForm, db_access: Session
) -> dict[str, str | None]:
    try:
        _user: User = await authenticate_by_identifier(
            identifier=user_to_sign_in.identifier, session=db_access
        )

        if not bool(_user):
            raiseHttpError(
                message=f"can not get account for `{user_to_sign_in.identifier}`",
                status_code=404,
            )

        if not await verify_password(
            hashed_password=_user.password, password=user_to_sign_in.password
        ):
            raiseHttpError(
                message="wrong password. request new password if you forgot it already.",
                status_code=401,
            )

        print(
            f"bearer_token: Bearer {await create_access_token(data_to_encode=_user.id)}"
        )
        return {"token": await create_access_token(data_to_encode=_user.id)}

    except Exception as error:
        raise error
