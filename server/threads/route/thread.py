from fastapi import APIRouter, HTTPException

from core.depedencies import DATABASE_SESSION_DEPENDENCY
from threads.controller.thread import ChainController
from utils.response import ResponseAPI


class ChainRoutes:
    def __init__(self):
        self.router = (APIRouter(),)
        self.session = DATABASE_SESSION_DEPENDENCY
        self.ChainController = ChainController(self.session)

    async def get_all(self):
        try:
            request = await self.ChainController.get_all()

            if request is not None:
                return ResponseAPI(
                    data=request,
                    message="all threads",
                    status_code=200,
                    success=True,
                ).response()

        except Exception as error:
            return ResponseAPI(
                message=f"An error occured: {error}",
                status_code=500,
                success=False,
            ).response()
