import datetime

from pydantic import BaseModel


class FeedbackBase(BaseModel):
    """Feedback Base Serializer"""
    content: str


class FeedbackRead(FeedbackBase):
    """Feedback Read From DB"""
    created_time: datetime.datetime
    class Config:
        """Enable ORM"""
        orm_mode = True
