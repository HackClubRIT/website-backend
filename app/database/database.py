"""
Database Config
"""
from os import environ
from sqlalchemy import create_engine


def set_up_database(env_variable="DATABASE_URL"):
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


def update_instance(database, db_obj, serializer_obj):
    """Update the database object from serializer"""
    for var, value in vars(serializer_obj).items():
        if value:
            setattr(db_obj, var, value)

    commit_changes_to_object(database, db_obj)
