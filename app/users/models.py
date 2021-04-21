"""
Define db tables
"""
from sqlalchemy import Column, String, Boolean, Integer
from app.database import Base


class User(Base):
    """The user model"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
