from fastapi import APIRouter
from ..user.models.user import User
# from .services.auth_by_id import authenticate_by_identifier
from .services import *

router = APIRouter(prefix="/auth", tags=["authentication"])   
