from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .comment import Comment


class Reply(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, unique=True, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    author: str = Field()  # TODO: the author of the reply should be a user model
    content: str = Field()

    comment_id: UUID | None = Field(foreign_key="comment.id")
    comment: Optional["Comment"] = Relationship(back_populates="replies")

    parent_reply_id: UUID | None = Field(default=None, foreign_key="reply.id")
    parent_reply: Optional["Reply"] = Relationship(
        sa_relationship_kwargs={"remote_side": "Reply.id"}, back_populates="replies"
    )
    replies: list["Reply"] = Relationship(back_populates="parent_reply")

    def to_dict(self):
        return {
            "author": self.author,
            "comment_id": str(self.comment_id) if self.comment_id else None,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "id": str(self.id),
            "updated_at": self.updated_at.isoformat(),
        }
