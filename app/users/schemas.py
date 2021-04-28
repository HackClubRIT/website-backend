"""
Define serializers
"""
from typing import Optional

from pydantic import BaseModel, validator
from app.commons.validators import email_validator, name_validator
from app.users.roles import Roles


class UserBase(BaseModel):
    """Base serializer"""
    username: str
    role: Roles
    name: str


class UserCreate(UserBase):
    """User write serializer(Can also be used for login)"""
    password: str

    @validator("name", check_fields=False)
    def is_valid_name(cls, name):
        if name_validator(name) is None:
            raise AssertionError("Name contains invalid characters")
        return name


class UserUpdate(BaseModel):
    """Update Serializer"""
    username: Optional[str]
    password: Optional[str]
    name: Optional[str]

    @validator("name", check_fields=False)
    def is_valid_name(cls, name):
        if name:
            if name_validator(name) is None:
                raise AssertionError("Name contains invalid characters")
            return name


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
