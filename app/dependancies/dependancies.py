"""
Common methods
"""
from app.database import SessionLocal


def get_db():
    """
    Get the current db session
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
