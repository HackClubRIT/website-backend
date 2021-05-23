"""
Application Model
"""
from sqlalchemy import Column, String, Integer, func, JSON, Enum
from app.database.config_db import Base
from .application_states import ApplicationStates
from app.commons.model_fields import AwareDateTime


class Application(Base):
    """New member application"""
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    created_date = Column(AwareDateTime, default=func.now())
    email = Column(String)
    name = Column(String)
    data = Column(JSON)
    status = Column(Enum(ApplicationStates), default=ApplicationStates.PENDING)
