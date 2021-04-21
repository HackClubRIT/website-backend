"""
CRUD the user table
"""
from sqlalchemy.orm import Session
from . import models, schemas


def get_user(database: Session, user_id: int):
    """Get User By ID"""
    return database.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(database: Session, username: str):
    """Get User By Username"""
    return database.query(models.User).filter(models.User.username == username).first()


def create_user(database: Session, user: schemas.UserWrite):
    """Create User"""
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(username=user.username, hashed_password=fake_hashed_password)
    database.add(db_user)
    database.commit()
    database.refresh(db_user)
    return db_user
