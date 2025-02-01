from typing import Annotated

from pydantic import AfterValidator, EmailStr
from sqlmodel import VARCHAR, Column, Field, SQLModel

from ..services.validate_password import validate_password


class UserSignupForm(SQLModel):
    email: EmailStr = Field(
        ...,
        title="email",
        sa_column=Column(
            "email",
            VARCHAR,
            unique=True,
            index=True,
        ),
        description="`USER` `email`",
    )

    firstname: str = Field(
        ..., min_length=3, max_length=50, description="`USER` `firstname`"
    )

    lastname: str = Field(
        ..., min_length=3, max_length=50, description="`USER` `lastname`"
    )

    password: Annotated[
        str,
        Field(
            ...,
            min_length=8,
            max_length=100,
            description="`USER` `password`",
            schema_extra={"examples": ["MyStr0ngP@ssword!"]},
        ),
        AfterValidator(validate_password),
    ]


class TokenPayload(SQLModel):
    sub: str | None = None
