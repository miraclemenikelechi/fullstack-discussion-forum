from fastapi import APIRouter
from .model import ThreadCreate

router = APIRouter(prefix="/threads")


@router.get("/threads")
async def get_thread():
    return "get all"


@router.post("/new")
async def create_thread(data: ThreadCreate):
    return data
