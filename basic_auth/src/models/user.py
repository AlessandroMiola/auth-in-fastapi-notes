from pydantic import EmailStr
from sqlalchemy.orm import declared_attr
from sqlmodel import AutoString, Field, SQLModel


class UserBase(SQLModel):
    # https://github.com/tiangolo/sqlmodel/discussions/730
    username: EmailStr = Field(primary_key=True, unique=True, sa_type=AutoString)


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    pass


class User(UserResponse, table=True):
    hashed_password: str

    @declared_attr
    def __tablename__(cls) -> str:
        return "basic_" + cls.__name__.lower() + "s"
