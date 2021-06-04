"""
Content Schemas
"""
import datetime
from typing import Optional

from pydantic import BaseModel, AnyUrl
from app.commons.serializer_field_mixins import NameMixin
from app.users.schemas import UserMinimal


class FeedbackBase(BaseModel):
    """Feedback Base Serializer"""
    content: str


class FeedbackRead(FeedbackBase):
    """Feedback Read From DB"""
    created_time: datetime.datetime
    id: int

    class Config:
        """Enable ORM"""
        orm_mode = True


class EventBaseSerializer(NameMixin):
    """Base Event Serializer"""
    registration_link: AnyUrl
    description: str
    date: datetime.datetime


class EventUpdateSerializer(NameMixin):
    name: Optional[str]
    registration_link: Optional[AnyUrl]
    description: Optional[str]
    date: Optional[datetime.datetime]


class EventReadSerializer(EventBaseSerializer):
    """Event Read from db serializer"""
    image_url: AnyUrl
    user: UserMinimal

    class Config:
        """Enable ORM"""
        orm_mode = True
