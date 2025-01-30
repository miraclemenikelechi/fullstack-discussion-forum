from typing import Any

import jwt
from pydantic import BaseModel

from core.config import appConfig
from utils.response import raiseHttpError


class TokenPayload(BaseModel):
    sub: str | None = None


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
