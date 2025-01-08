from fastapi import APIRouter
from .model import ThreadCreate

router = APIRouter(prefix="/threads", tags=["thread"])


@router.get("/threads")
async def get_all_threads():
    return "get all"


@router.get("/{slug}")
async def get_thread(slug: str):
    return f"get {slug}"


@router.post("/new")
async def create_thread(data: ThreadCreate):
    return data


@router.patch("/{slug}")
async def edit_thread(slug: str):
    pass


@router.delete("/{slug}")
async def delete_thread(slug: str):
    pass
