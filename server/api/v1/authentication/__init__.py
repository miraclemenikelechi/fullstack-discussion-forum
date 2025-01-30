from fastapi import APIRouter

from .routes.login import router as login
from .routes.signup import router as signup

router = APIRouter(prefix="/auth", tags=["authentication"])

# register routes under `/auth`
router.include_router(login)
router.include_router(signup)
