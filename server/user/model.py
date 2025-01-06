from enum import Enum
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserCreate(SQLModel):
    id: UUID = Field(default_factory=uuid4, unique=True, primary_key=True)
