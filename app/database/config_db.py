"""
Config Normal Database
"""
from sqlalchemy.orm import sessionmaker, declarative_base
from .database import set_up_database

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=set_up_database())

Base = declarative_base()
