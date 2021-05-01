"""
Config Normal Database
"""
from sqlalchemy.orm import sessionmaker, declarative_base
from os import environ
from .database import set_up_database

if environ.get("DATABASE_URL"):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=set_up_database())
else:
    print("WARNING: No Production DB Detected")

Base = declarative_base()
