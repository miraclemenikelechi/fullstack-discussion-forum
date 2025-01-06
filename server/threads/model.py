from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Reply(SQLModel):
    id: UUID = Field(default_factory=uuid4, unique=True, primary_key=True)

    content: str
    thread_id: UUID | None = Field(default=None)


class ThreadCreate(SQLModel):
    title: str = Field()
    description: str = Field()
    author: str = Field()

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ThreadBase(SQLModel):
    id: uuid4

    replies: list[Reply]
