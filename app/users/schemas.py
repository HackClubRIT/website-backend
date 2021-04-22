"""
Define serializers
"""
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    """Base serializer"""
    username: str


class UserCreate(UserBase):
    """User write serializer(Can also be used for login)"""
    password: str


class UserUpdate(BaseModel):
    """Update Serializer"""
    username: Optional[str]
    password: Optional[str]


class User(UserBase):
    """User read serializer(ORM)"""
    id: int
    is_active: bool

    class Config:
        """Enable ORM"""
        orm_mode = True


class UserInDB(User):
    """Mocks User Table"""
    password: str


class Token(BaseModel):
    """Token Serializer"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Data encrypted by token"""
    username: Optional[str] = None
