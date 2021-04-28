"""
Application Serializers
"""
import datetime
from pydantic import BaseModel, validator
from app.applications.application_states import ApplicationStates
from app.commons.validators import name_validator, email_validator


class ApplicationBase(BaseModel):
    """Base application serializer"""
    email: str
    data: dict
    name: str

    @validator("email")
    def is_valid_email(cls, email):
        assert email_validator(email) is not None
        return email

    @validator("name")
    def is_valid_name(cls, name):
        assert name_validator(name) is not None
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
