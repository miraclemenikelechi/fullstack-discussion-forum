from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from api.v1.user.models.user import User

    from .reply import Reply
    from .thread import Thread


class Comment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, unique=True, primary_key=True, index=True)

    author_id: Optional[UUID] = Field(foreign_key="user.id")
    author: Optional["User"] = Relationship(back_populates="comments")

    content: str = Field(...)
    replies: list["Reply"] = Relationship(back_populates="comment")
    thread_id: Optional[UUID] = Field(default=None, foreign_key="thread.id")
    thread: Optional["Thread"] = Relationship(back_populates="comments")

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def to_dict(self):
        return {
            "author": self.author.username,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "id": str(self.id),
            "replies": [reply.to_dict() for reply in self.replies]
            if self.replies
            else [],
            "thread_id": str(self.thread_id) if self.thread_id else None,
            "updated_at": self.updated_at.isoformat(),
        }

    def serialize(self, depth=1, exclude=None, include=None):
        from utils.model import serialize_model

        return serialize_model(
            depth=depth, exclude=exclude, include=include, table_instance=self
        )


class CommentCreateForm(SQLModel):
    content: str = Field(..., min_length=10, description="Thread content")
