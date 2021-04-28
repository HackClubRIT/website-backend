"""
CRUD applications table
"""
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.database.database import commit_changes_to_object
from . import models
from .schemas import ApplicationBase
from .application_states import ApplicationStates


def get_application(database: Session, application_id: int):
    """Get Application By ID"""
    return database.query(models.Application).\
        filter(models.Application.id == application_id).first()


def get_pending_applications(database: Session):
    """Get All Pending Applications"""
    return database.query(models.Application).\
        filter(models.Application.status == ApplicationStates.PENDING).all()


def get_latest_application_by_email(database: Session, email: str):
    """Get Latest Application Of an Email"""
    return database.query(models.Application).filter(models.Application.email == email)\
        .order_by(desc(models.Application.created_date)).limit(1).first()


def create_application(database: Session, application: ApplicationBase):
    """Create new application"""
    db_application = models.Application(
        data=application.data,
        email=application.email,
        name=application.name
    )
    commit_changes_to_object(database=database, obj=db_application)
    return db_application


def change_state_of_application(
        database: Session,
        application_id: int,
        new_state: ApplicationStates
):
    """Approve/Reject Application"""
    db_application = get_application(database, application_id)
    if db_application:
        db_application.status = new_state
        commit_changes_to_object(database, db_application)
        return db_application
    return None
