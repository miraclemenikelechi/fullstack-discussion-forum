from sqlmodel import SQLModel, Field


class UserSignIn(SQLModel):
    identifier: str = Field(..., description="User email or username")
    password: str = Field(...)
