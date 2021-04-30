"""
Application Serializers
"""
# pylint: disable=no-self-argument,no-self-use
import datetime
from pydantic import BaseModel, validator, ValidationError
from app.applications.application_states import ApplicationStates
from app.commons.validators import name_validator, email_validator


class ApplicationBase(BaseModel):
    """Base application serializer"""
    email: str
    data: dict
    name: str

    @validator("email")
    def is_valid_email(cls, email):
        """
        Validate Email
        :raise AssertionError
        """
        if email_validator(email) is None:
            raise ValidationError("Invalid Email")
        return email

    @validator("name")
    def is_valid_name(cls, name):
        """
        Validate Name
        :raise AssertionError
        """
        if name_validator(name) is None:
            raise ValidationError("Name contains invalid characters")
        return name


class ApplicationUpdate(BaseModel):
    """Update serializer"""
    approved: bool


class ApplicationRead(ApplicationBase):
    """Read serializer"""
    id: int
    status: ApplicationStates
    created_date: datetime.datetime

    class Config:
        """Enable ORM"""
        orm_mode = True
