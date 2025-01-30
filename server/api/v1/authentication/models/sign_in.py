from sqlmodel import Field, SQLModel

from core.constants import PATTERNS


class UserSignInForm(SQLModel):
    identifier: str = Field(..., description="`USER` `email` or `username`", gt=3)

    password: str = Field(
        ..., gt=6, regex=PATTERNS["PASSWORD"], description="`USER` `password`"
    )
