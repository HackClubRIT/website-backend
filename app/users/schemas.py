"""
Define serializers
"""
# pylint: disable=no-self-argument, no-self-use
from typing import Optional
from pydantic import BaseModel, validator, constr
from app.commons.validators import name_validator
from app.users.roles import Roles


class BaseSerializer(BaseModel):
    """
    Common Validators
    """
    @validator("name", check_fields=False)
    def is_valid_name(cls, name):
        """
        Is valid name?
        :raise AssertionError
        """
        if name:
            if name_validator(name) is None:
                raise AssertionError("Name contains invalid characters")
        return name


class UserBase(BaseSerializer):
    """Base serializer"""
    username: str
    role: Roles
    name: str


class UserCreate(UserBase):
    """User write serializer(Can also be used for login)"""
    password: constr(min_length=8)


class UserUpdate(BaseSerializer):
    """Update Serializer"""
    username: Optional[str]
    password: Optional[str]
    name: Optional[str]


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
