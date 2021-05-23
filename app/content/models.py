"""
The event model
"""
from sqlalchemy import Column, String, func, Integer
from app.commons.model_fields import AwareDateTime
from app.database.config_db import Base

"""
class Event(Base):
    #Event Model
    __tablename__ = "events"
    datetime = Column(AwareDateTime, nullable=False)
    name = Column(String, nullable=False)
    winner = Column(String, nullable=True)
"""

class Feedback(Base):
    """Feedback model"""
    __tablename__ = "feedbacks"
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    created_time = Column(AwareDateTime, nullable=False, default=func.now())