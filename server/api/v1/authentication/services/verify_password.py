from core.config import appConfig


async def verify_password(password: str, hashed_password: str) -> bool:
    return appConfig.PASSWORD_CONTEXT.verify(password, hashed_password)
