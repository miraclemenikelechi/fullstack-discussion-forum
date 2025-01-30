from core.config import appConfig


async def hash_password(password: str) -> str:
    return appConfig.PASSWORD_CONTEXT.hash(password)
