from uuid import UUID

import strawberry


@strawberry.type
class ReplyType:
    content: str
    tagged_users: list | None
    user: str


@strawberry.type
class CreateThreadType:
    id: UUID

    author: str
    content: str
    title: str
