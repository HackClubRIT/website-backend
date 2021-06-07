"""
Content Schemas
"""
import datetime
from typing import Optional
from pydantic import BaseModel, AnyUrl
from app.commons.serializer_field_mixins import NameMixin, ImageMixin, UserMinimalMixin


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
    image_id: int


class EventUpdateSerializer(NameMixin):
    """Event Update Serializer"""
    name: Optional[str]
    registration_link: Optional[AnyUrl]
    description: Optional[str]
    date: Optional[datetime.datetime]
    image_id: Optional[int]


class EventReadSerializer(EventBaseSerializer, ImageMixin, UserMinimalMixin):
    """Event Read from db serializer"""
    id: int

    class Config:
        """Enable ORM"""
        orm_mode = True


class ImageReadSerializer(BaseModel):
    """Serialize Image"""
    id: int
    url: AnyUrl

    class Config:
        """Config"""
        orm_mode = True
