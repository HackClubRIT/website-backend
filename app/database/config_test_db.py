"""
Config Test Database
"""
from sqlalchemy.orm import sessionmaker

from app.database.database import set_up_database

engine = set_up_database("TEST_DB", fail_silently=True)

if engine:
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    TestingSessionLocal = None

