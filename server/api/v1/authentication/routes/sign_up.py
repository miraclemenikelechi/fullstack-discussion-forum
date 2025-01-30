from fastapi import APIRouter

from core.depedencies import DATABASE_SESSION_DEPENDENCY

from ..models import UserSignupForm

router = APIRouter()


@router.post(path="/signup", status_code=201)
async def signup(data: UserSignupForm, session: DATABASE_SESSION_DEPENDENCY):  # type: ignore
    pass
