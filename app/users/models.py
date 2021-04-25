"""
Define db tables
"""
from sqlalchemy import Column, String, Boolean, Integer, Enum
from app.database import Base
from app.users.roles import Roles


class User(Base):
    """The user model"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(Roles), default=Roles.USER)
