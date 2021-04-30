"""
Config Test Database
"""
from sqlalchemy.orm import sessionmaker

from app.database.database import set_up_database

engine = set_up_database("TEST_DB")

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

