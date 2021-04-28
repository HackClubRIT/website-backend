"""
Application Serializers
"""
import datetime
from pydantic import BaseModel

from app.applications.application_states import ApplicationStates


class ApplicationBase(BaseModel):
    """Base application serializer"""
    email: str
    data: dict


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
