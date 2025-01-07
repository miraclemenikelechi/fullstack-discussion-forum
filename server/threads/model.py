from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel
from pydantic import BaseModel


class Reply(SQLModel):
    id: UUID = Field(default_factory=uuid4, unique=True, primary_key=True)

    content: str
    thread_id: UUID | None = Field(default=None)


class ThreadCreate(BaseModel):
    title: str = Field()
    description: str = Field()
    author: str = Field()


class ThreadBase(SQLModel):
    id: uuid4

    replies: list[Reply]

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
