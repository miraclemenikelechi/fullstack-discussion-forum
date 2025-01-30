from typing import Any

import jwt

from core.config import appConfig
from utils.response import raiseHttpError

from ..models.signup import TokenPayload


def verify_access_token(access_token: str) -> Any | None:
    try:
        payload = jwt.decode(
            jwt=access_token,
            key=appConfig.SECRET_KEY,
            algorithms=[appConfig.ALGORITHM],
        )

        return TokenPayload(**payload)

    except Exception as error:
        raiseHttpError(message=f"{error}", status_code=417)
