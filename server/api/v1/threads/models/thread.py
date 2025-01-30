from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .comment import Comment    


class Thread(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, unique=True, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    author_id: str = Field()  # TODO: the author of the thread should be a user model
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
