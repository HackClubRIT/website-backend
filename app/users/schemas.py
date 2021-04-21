"""
Define serializers
"""
from pydantic import BaseModel


class UserBase(BaseModel):
    """Base serializer"""
    username: str


class UserCreate(UserBase):
    """User write serializer"""
    password: str


class User(UserBase):
    """User read serializer(ORM)"""
    id: int
    is_active: bool

    class Config:
        """Enable ORM"""
        orm_mode = True
