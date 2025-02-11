from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from api.v1.threads.models.comment import Comment
from api.v1.threads.models.reply import Reply
from api.v1.threads.models.thread import Thread
from utils.model import serialize_model


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(SQLModel, table=True):
    id: UUID = Field(
        ..., default_factory=uuid4, unique=True, primary_key=True, index=True
    )

    email: str = Field(..., unique=True, index=True)
    firstname: str = Field(...)
    lastname: str = Field(...)
    password: str = Field(...)

    registered_at: datetime = Field(..., default_factory=datetime.now)
    role: UserRole = Field(default=UserRole.USER)
    username: str = Field(..., unique=True, index=True)

    comments: list["Comment"] = Relationship(back_populates="author")
    replies: list["Reply"] = Relationship(back_populates="author")
    threads: list["Thread"] = Relationship(back_populates="author")

    def serialize(self, include=None, depth=1):
        return serialize_model(
            depth=depth,
            exclude={"password", "role"},
            include=include,
            table_instance=self,
        )


# include={"threads": True}
