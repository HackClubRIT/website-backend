"""
Database Config
"""
from os import environ
from sqlalchemy import create_engine


def set_up_database(env_variable="DATABASE_URL", fail_silently=False):
    """Set up connection to a db"""
    database_url = environ.get(env_variable)

    try:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
    except AttributeError:
        print("NO TEST DB")
        return None
    return create_engine(database_url)


def commit_changes_to_object(database, obj):
    """Finish the database transaction and refresh session"""
    database.add(obj)
    database.commit()
    database.refresh(obj)
