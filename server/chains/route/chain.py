from fastapi import APIRouter, Depends, HTTPException

from chains import router
from chains.controller.chain import ChainController
from core.depedencies import DATABASE_SESSION_DEPENDENCY, CURRENT_USER_DEPENDENCY

# from threads.controller.thread import ChainController
from threads.model import ThreadCreate
from utils.response import ResponseAPI, ResponseApiModel, ResponseDataModel


class ChainRoutes:
    def __init__(self):
        self.router = router

        # router
        self.router.add_api_route(
            "/",
            self.get_all,
            methods=["GET"],
            status_code=200,
            # responses={404: {"description": "Not found"}},
            response_model=ResponseDataModel,
        )

        self.router.add_api_route(
            "/",
            self.create,
            methods=["POST"],
            status_code=201,
            response_model=ResponseApiModel,
        )

    async def get_all(self, db: DATABASE_SESSION_DEPENDENCY):  # type: ignore
        try:
            request = await ChainController(db=db).get_all()

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

    async def create(
        data: ThreadCreate,
        db: DATABASE_SESSION_DEPENDENCY,  # type: ignore
        current_user: CURRENT_USER_DEPENDENCY,  # type: ignore
    ):
        # try:
        #     request = await ChainController(db=db).create(data=data, user=current_user)

        #     if request is not None:
        #         return ResponseAPI(
        #             data=request,
        #             message=f"thread `{request['id']}` by user `{request['author_username']}` has been created!",
        #             status_code=201,
        #             success=True,
        #         )

        # except Exception as error:
        #     return ResponseAPI(
        #         message=f"An error occured: {error}",
        #         status_code=500,
        #         success=False,
        #     ).response()

        pass


chain_routes = ChainRoutes()
