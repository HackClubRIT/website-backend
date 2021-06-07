"""
Define db tables
"""
from sqlalchemy import Column, String, Boolean, Integer, Enum
from app.database.config_db import Base
from app.users.roles import Roles


class User(Base):
    """The user model"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(Enum(Roles), default=Roles.USER, nullable=False)
