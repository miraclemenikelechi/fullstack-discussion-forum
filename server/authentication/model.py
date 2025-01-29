import re
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import AfterValidator, EmailStr
from sqlmodel import Field, SQLModel, Column, VARCHAR

from core.constants import PATTERNS


def validate_password(password: str) -> str:
    try:
        if not re.match(pattern=PATTERNS["PASSWORD"], string=password):
            raise ValueError(
                "Password must contain at least 1 digit, 1 lowercase, 1 uppercase, 1 special character, and be between 8-64 characters long."
            )

        return password

    except Exception as error:
        raise error


class UserLogin(SQLModel):
    identifier: str = Field(...)
    password: str = Field(...)


class UserSignup(SQLModel):
    email: EmailStr = Field(
        ...,
        title="email",
        sa_column=Column(
            "email",
            VARCHAR,
            unique=True,
            index=True,
        ),
        description="User email",
    )
    firstname: str = Field(
        ..., min_length=3, max_length=50, description="User first name"
    )
    lastname: str = Field(
        ..., min_length=3, max_length=50, description="User last name"
    )
    password: Annotated[
        str,
        Field(
            ...,
            min_length=8,
            max_length=100,
            description="The user's password.",
            schema_extra={"examples": ["MyStr0ngP@ssword!"]},
        ),
        AfterValidator(validate_password),
    ]


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, unique=True, primary_key=True, index=True)

    username: str = Field(..., unique=True, index=True)
    firstname: str = Field(...)
    lastname: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)

    def to_dict(self):
        return self.model_dump().pop("password", None)
