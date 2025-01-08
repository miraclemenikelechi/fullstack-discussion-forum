from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


# thread model to represent a discussion thread
class Thread(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, unique=True, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    author: str = Field()  # TODO: the author of the thread should be a user model
    content: str = Field()
    title: str = Field()

    comments: list["Comment"] = Relationship(back_populates="thread")


# comment model to represent a comment on a thread
class Comment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, unique=True, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    author: str = Field()  # TODO: the author of the comment should be a user model
    content: str = Field()

    thread: Thread | None = Relationship(back_populates="comments")
    thread_id: UUID | None = Field(default=None, foreign_key="thread.id")
    replies: list["Reply"] = Relationship(back_populates="comment")


# reply model to represent a reply to a comment on a thread
class Reply(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, unique=True, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    author: str = Field()  # TODO: the author of the reply should be a user model
    content: str = Field()

    comment_id: UUID | None = Relationship(back_populates="comment.id")


class ThreadCreate(BaseModel):
    author: str = Field()
    description: str = Field()
    title: str = Field()
