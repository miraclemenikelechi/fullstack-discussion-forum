from utils.response import raiseHttpError

from .. import User, authenticate_by_identifier, verify_password, create_access_token


async def sign_in_a_user(user_to_sign_in, db_access) -> dict[str, str | None]:
    try:
        user_exists: User = await authenticate_by_identifier(
            identifier=user_to_sign_in.identifier, session=db_access
        )

        if not bool(user_exists):
            raiseHttpError(
                message=f"can not get account for `{user_to_sign_in.identifier}`",
                status_code=404,
            )

        if not await verify_password(
            hashed_password=user_exists.password, password=user_to_sign_in.password
        ):
            raiseHttpError(
                message="wrong password. request new password if you forgot it already.",
                status_code=401,
            )

        return {"token": await create_access_token(data_to_encode=user_exists.id)}

    except Exception as error:
        raise error
