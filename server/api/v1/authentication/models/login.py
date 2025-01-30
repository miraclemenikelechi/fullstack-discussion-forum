from sqlmodel import Field, SQLModel

from core.constants import PATTERNS


class UserLoginForm(SQLModel):
    identifier: str = Field(
        ..., description="`USER` `email` or `username`", min_length=3
    )

    password: str = Field(
        ..., min_length=8, regex=PATTERNS["PASSWORD"], description="`USER` `password`"
    )
