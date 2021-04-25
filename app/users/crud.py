"""
CRUD the user table & hashing passwords
"""
# Disabled as it will cause errors with boolean field comparison
# pylint: disable=singleton-comparison

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    """Hash the password"""
    return pwd_context.hash(password)


def verify_password(user, password):
    """
    verify password is correct
    :param user: Model User
    :param password: Plaintext password
    """
    return pwd_context.verify(password, user.password)


def _commit_changes_to_object(database, user_obj):
    """Finish the database transaction and refresh session"""
    database.add(user_obj)
    database.commit()
    database.refresh(user_obj)


def get_user(database: Session, user_id: int):
    """Get User By ID"""
    return database.query(models.User).filter(models.User.id == user_id,
                                              models.User.is_active == True).first()


def get_user_by_username(database: Session, username: str, all_users=False):
    """
    Get User By Username
    :param all_users: check all users in db including inactive ones
    """
    if all_users:
        return database.query(models.User).filter(models.User.username == username).first()
    return database.query(models.User).filter(models.User.username == username,
                                              models.User.is_active == True).first()


def create_user(database: Session, user: schemas.UserCreate):
    """
    Create User
    Development Only
    """
    db_user = models.User(
        username=user.username,
        password=hash_password(user.password),
        role=user.role
    )
    _commit_changes_to_object(database, db_user)
    return db_user


def update_user(database: Session, user_updated: schemas.UserUpdate, user_id: int):
    """Update User"""
    db_user = get_user(database, user_id)
    if db_user is None:
        return None

    if getattr(user_updated, "password"):
        user_updated.password = hash_password(user_updated.password)

    for var, value in vars(user_updated).items():
        if value:
            setattr(db_user, var, value)

    _commit_changes_to_object(database, db_user)
    return db_user


def delete_user(database: Session, user_id: int):
    """
    Soft delete User
    sets is_active to false
    """
    db_user = get_user(database, user_id)
    if db_user:
        db_user.is_active = False
        _commit_changes_to_object(database, db_user)
        return True
    return None
