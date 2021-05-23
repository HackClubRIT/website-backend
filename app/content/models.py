"""
The event model
"""
from sqlalchemy import Column, String, func, Integer
from app.commons.model_fields import AwareDateTime
from app.database.config_db import Base

class Feedback(Base):
    """Feedback model"""
    __tablename__ = "feedbacks"
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    created_time = Column(AwareDateTime, nullable=False, default=func.now())
