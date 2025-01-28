from enum import Enum
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, unique=True, primary_key=True, index=True)

    username: str = Field(..., unique=True, index=True)
    firstname: str = Field(...)
    lastname: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
