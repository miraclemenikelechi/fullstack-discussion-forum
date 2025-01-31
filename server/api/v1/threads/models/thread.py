from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from api.v1.user.models.user import User

    from .comment import Comment


class Thread(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, unique=True, primary_key=True, index=True)

    author_id: Optional[UUID] = Field(foreign_key="user.id")
    author: Optional["User"] = Relationship(back_populates="threads")

    comments: list["Comment"] = Relationship(back_populates="thread")

    content: str = Field()
    title: str = Field()

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def serialize(self) -> dict[str, Any]:
        model: dict[str, Any] = self.model_dump(
            exclude={"created_at", "updated_at"}, mode="json"
        )

        model["author"] = self.author.username
        model["comments"] = (
            [comment.to_dict() for comment in self.comments] if self.comments else []
        )

        return model


class ThreadCreate(SQLModel):
    content: str = Field(..., min_length=10, description="`THREAD` `content`")

    title: str = Field(
        ..., min_length=5, max_length=100, description="`THREAD` `title`"
    )
