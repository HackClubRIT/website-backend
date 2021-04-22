"""
CRUD the user table
"""
from sqlalchemy.orm import Session
from . import models, schemas


def hash_password(password):
    """Hash the password"""
    # TODO
    return password


def verify_password(user, password):
    """
    verify password is correct
    :param user: Model User
    """
    return hash_password(password) == user.password


def get_user(database: Session, user_id: int):
    """Get User By ID"""
    return database.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(database: Session, username: str):
    """Get User By Username"""
    return database.query(models.User).filter(models.User.username == username).first()


def create_user(database: Session, user: schemas.UserCreate):
    """Create User"""
    db_user = models.User(username=user.username, password=hash_password(user.password))
    database.add(db_user)
    database.commit()
    database.refresh(db_user)
    return db_user


def update_user(database: Session, user: schemas.UserUpdate, user_id: int):
    """Update User"""
    db_user = get_user(database, user_id)
    if db_user is None:
        # TODO
        pass
    if getattr(user, "password"):
        user.password = hash_password(user.password)

    for var, value in vars(user).items():
        setattr(db_user, var, value) if value else None

    database.add(db_user)
    database.commit()
    database.refresh(db_user)
    return db_user
