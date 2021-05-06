"""
Config Test Database
"""
from sqlalchemy.orm import sessionmaker

from app.database.database import set_up_database

engine = set_up_database("TEST_DB")

if engine:
    TESTING_SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    TESTING_SESSION_LOCAL = None
