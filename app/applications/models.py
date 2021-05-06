"""
Application Model
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, func, DateTime, JSON, Enum, TypeDecorator
from dateutil.tz import gettz
from app.database.config_db import Base
from app.settings import TZ
from .application_states import ApplicationStates


class AwareDateTime(TypeDecorator):
    # pylint: disable=abstract-method
    """Custom field to handle timezones"""

    @property
    def python_type(self):
        """python type"""
        return datetime

    impl = DateTime

    def process_bind_param(self, value, dialect):
        """Convert to UTC time before saving"""
        if value.tzinfo is None:
            # Set native timezone objects to default TZ
            value = value.replace(tzinfo=gettz(TZ))
        return value

    def process_result_value(self, value, dialect):
        """Convert to TZ after fetching as UTC from DB"""
        return value.replace(tzinfo=gettz(TZ))


class Application(Base):
    """New member application"""
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    created_date = Column(AwareDateTime, default=func.now())
    email = Column(String)
    name = Column(String)
    data = Column(JSON)
    status = Column(Enum(ApplicationStates), default=ApplicationStates.PENDING)
