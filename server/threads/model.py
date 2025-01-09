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

    def to_dict(self):
        return {
            "id": str(self.id),
            "author": self.author,
            "comments": [comment.to_dict() for comment in self.comments]
            if self.comments
            else [],
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "title": self.title,
            "updated_at": self.updated_at.isoformat(),
        }


# comment model to represent a comment on a thread
class Comment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, unique=True, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    author: str = Field()  # TODO: the author of the comment should be a user model
    content: str = Field()

    replies: list["Reply"] = Relationship(back_populates="comment")
    thread_id: UUID | None = Field(default=None, foreign_key="thread.id")
    thread: Thread | None = Relationship(back_populates="comments")

    def to_dict(self):
        return {}


# reply model to represent a reply to a comment on a thread
class Reply(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, unique=True, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    author: str = Field()  # TODO: the author of the reply should be a user model
    content: str = Field()

    comment_id: UUID | None = Field(foreign_key="comment.id")
    comment: Comment | None = Relationship(back_populates="replies")

    def to_dict(self):
        return {}


# requests


class ThreadCreate(SQLModel):
    author: str = Field(..., min_length=3, max_length=50, description="Author name")
    content: str = Field(..., min_length=10, description="Thread content")
    title: str = Field(..., min_length=5, max_length=100, description="Thread title")


class CommentCreate:
    author: str = Field()
    content: str = Field()


class ReplyCreate:
    author: str = Field()
    content: str = Field()


# responses


class CommentsResponse(BaseModel):
    pass


class AllThreadsResponse(BaseModel):
    id: str
    author: str
    comments: list[CommentsResponse]
    content: str
    created_at: str
    title: str
