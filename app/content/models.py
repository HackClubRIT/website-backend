"""
The event model
"""
from sqlalchemy import Column, String, func, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.commons.model_fields import AwareDateTime
from app.database.config_db import Base


class Feedback(Base):
    """Feedback model"""
    __tablename__ = "feedbacks"
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    created_time = Column(AwareDateTime, nullable=False, default=func.now())


class Event(Base):
    """Event model"""
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    date = Column(AwareDateTime, nullable=False)
    registration_link = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
