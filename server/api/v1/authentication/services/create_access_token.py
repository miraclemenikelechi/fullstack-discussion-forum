from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from core.config import appConfig
from utils.response import raiseHttpError


async def create_access_token(data_to_encode: str | Any) -> str | None:
    expiry_time = datetime.now(timezone.utc) + timedelta(
        minutes=appConfig.VALID_TOKEN_IN_MINUTES
    )

    to_encode: dict[str, Any] = {
        "exp": expiry_time,
        "sub": str(data_to_encode),
    }

    try:
        return jwt.encode(
            payload=to_encode,
            key=appConfig.SECRET_KEY,
            algorithm=appConfig.ALGORITHM,
        )

    except Exception as error:
        raiseHttpError(message=f"{error}", status_code=417)
