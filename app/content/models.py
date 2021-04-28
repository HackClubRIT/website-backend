from sqlalchemy import Column, DateTime, String
from app.database import Base


class Event(Base):
    """Event Model"""
    datetime = Column(DateTime, nullable=False)
    name = Column(String, nullable=False)
    winner = Column(String, nullable=True)


