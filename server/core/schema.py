from datetime import datetime
from uuid import UUID

import strawberry


@strawberry.type
class ReplyType:
    id: UUID
    created_at: datetime
    updated_at: datetime

    content: str
    author: str


@strawberry.type
class CommentType:
    id: UUID
    created_at: datetime
    updated_at: datetime

    content: str
    author: str

    replies: list[ReplyType]


@strawberry.type
class ThreadType:
    id: UUID
    created_at: datetime
    updated_at: datetime

    author: str
    content: str
    title: str

    comments: list[CommentType]


@strawberry.type
class Query:
    pass
