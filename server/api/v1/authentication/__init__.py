from fastapi import APIRouter

from ..user.models.user import User  # noqa: F401
from .services import *  # noqa: F403

router = APIRouter(prefix="/auth", tags=["authentication"])
