"""
Define serializers
"""
from pydantic import BaseModel


class UserBase(BaseModel):
    """Base serializer"""
    username: str


class UserWrite(UserBase):
    """User write serializer(Can also be used for login)"""
    password: str


class User(UserBase):
    """User read serializer(ORM)"""
    id: int
    is_active: bool

    class Config:
        """Enable ORM"""
        orm_mode = True
