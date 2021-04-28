"""
Application Model
"""
from sqlalchemy import Column, String, Integer, func, DateTime, JSON, Enum
from app.database import Base
from .application_states import ApplicationStates


class Application(Base):
    """New member application"""
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime(timezone=True), default=func.now())
    email = Column(String)
    data = Column(JSON)
    status = Column(Enum(ApplicationStates), default=ApplicationStates.PENDING)
