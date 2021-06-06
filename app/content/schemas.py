"""
Content Schemas
"""
import datetime
from typing import Optional, Any
from pydantic import BaseModel, AnyUrl, validator
from app.commons.serializer_field_mixins import NameMixin
from app.users.schemas import UserMinimal, User


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
    image_url: AnyUrl


class EventUpdateSerializer(NameMixin):
    """Event Update Serializer"""
    name: Optional[str]
    registration_link: Optional[AnyUrl]
    description: Optional[str]
    date: Optional[datetime.datetime]
    image_url: Optional[AnyUrl]


class EventReadSerializer(EventBaseSerializer):
    """Event Read from db serializer"""
    image_url: AnyUrl
    user: User
    id: int

    @validator("user")
    def abstract_user(cls, user):
        return UserMinimal(name=user.name, id=user.id)

    class Config:
        """Enable ORM"""
        orm_mode = True
