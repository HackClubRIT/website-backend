"""
Application Model
"""
from sqlalchemy import Column, String, Integer, func, JSON, Enum
from app.database.config_db import Base
from app.commons.model_fields import AwareDateTime
from .application_states import ApplicationStates


class Application(Base):
    """New member application"""
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    created_date = Column(AwareDateTime, default=func.now(), nullable=False)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    data = Column(JSON, nullable=False)
    status = Column(Enum(ApplicationStates),
                    default=ApplicationStates.PENDING, nullable=False)
