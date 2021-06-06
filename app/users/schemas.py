"""
Define serializers
"""
from typing import Optional
from pydantic import BaseModel, constr
from app.commons.serializer_field_mixins import EmailMixin, NameMixin
from app.users.roles import Roles


class UserBase(EmailMixin, NameMixin):
    """Base serializer"""
    role: Roles


class UserCreate(UserBase):
    """User write serializer"""
    password: constr(min_length=8)


class UserUpdate(EmailMixin, NameMixin):
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


class UserLogin(EmailMixin):
    """Login Serializer"""
    password: constr(min_length=8)


class Token(BaseModel):
    """Token Serializer"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Data encrypted by token"""
    email: Optional[str] = None
