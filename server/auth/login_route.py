from fastapi import APIRouter
from .login_model import UserLogin

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login")
async def login(user_credentials: UserLogin):
    return user_credentials
