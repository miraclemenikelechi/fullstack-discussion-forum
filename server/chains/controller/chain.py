from sqlmodel import Session

from core import crud
from threads.model import Thread, ThreadCreate
from user.model import User


class ChainController:
    def __init__(self, db: Session):
        self.db = db
        self.model = Thread

    async def get_all(self):
        try:
            return [
                data.to_dict()
                for data in crud.transact_by_param(db=self.db, table=self.model)
            ]

        except Exception as error:
            raise error

    async def create(self, data: ThreadCreate, user: User):
        new_thread: Thread = {
            "author": str(user.id),
            "content": data.content,
            "title": data.title,
        }

        try:
            db_thread: Thread = crud.create(
                data=new_thread, db=self.db, table=self.model
            )

            return {
                "author_id": db_thread.author,
                "author_username": user.username,
                "comments": db_thread.comments,
                "content": db_thread.content,
                "id": str(db_thread.id),
                "title": db_thread.title,
            }

        except Exception as error:
            raise error
