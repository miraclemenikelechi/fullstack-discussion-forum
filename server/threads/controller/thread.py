from sqlmodel import Session

from core import crud
from threads.model import Thread


class ChainController:
    def __init__(self, db: Session):
        self.db = db
        self.model = Thread
        pass

    async def get_all(self):
        try:
            return [
                data.to_dict()
                for data in crud.transact_by_param(db=self.db, table=self.model)
            ]

        except Exception as error:
            raise error
