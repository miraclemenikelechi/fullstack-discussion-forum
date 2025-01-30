from fastapi import APIRouter

from ..user.models.user import User  # noqa: F401
from .routes.login import router as sign_in
from .routes.signup import router as sign_up
from .services import *  # noqa: F403

router = APIRouter(prefix="/auth", tags=["authentication"])

# register routes under `/auth`
router.include_router(sign_in)
router.include_router(sign_up)
