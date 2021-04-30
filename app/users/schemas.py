"""
Define serializers
"""
# pylint: disable=no-self-argument, no-self-use
from typing import Optional
from pydantic import BaseModel, validator, constr, ValidationError
from app.commons.validators import name_validator, email_validator
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
                raise ValidationError("Name contains invalid characters")
        return name

    @validator("email", check_fields=False)
    def is_valid_email(cls, email):
        """
        Is valid email?
        :raise AssertionError
        """
        if email:
            if email_validator(email) is None:
                raise ValidationError("Email is invalid")
            return email


class UserBase(BaseSerializer):
    """Base serializer"""
    email: str
    role: Roles
    name: str


class UserCreate(UserBase):
    """User write serializer(Can also be used for login)"""
    password: constr(min_length=8)


class UserUpdate(BaseSerializer):
    """Update Serializer"""
    email: Optional[str]
    password: Optional[constr(min_length=8)]
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
    password: constr(min_length=8)


class Token(BaseModel):
    """Token Serializer"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Data encrypted by token"""
    email: Optional[str] = None
