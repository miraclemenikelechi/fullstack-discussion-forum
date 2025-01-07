from typing import Annotated, Any, Generator

from fastapi import Depends
from sqlmodel import Session

from .database import db_engine


def db_session() -> Generator[Session, Any, None]:
    with Session(db_engine) as session:
        yield session


DATABASE_SESSION_DEPENDENCY: Session = Annotated[Session, Depends[db_session]]
