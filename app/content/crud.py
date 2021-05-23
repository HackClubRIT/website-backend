"""
CRUD Feedbacks, Events
"""
from sqlalchemy.orm import Session
from app.database.database import commit_changes_to_object
from .models import Feedback
from . import schemas


def get_all_feedback(database: Session):
    """Get all feedback from DB"""
    return database.query(Feedback).order_by(Feedback.created_time.desc()).all()

def get_feedback_by_id(database: Session, unique_id: int):
    """Get feedback by id from DB"""
    return database.query(Feedback).filter(Feedback.id == unique_id).first()

def create_feedback(database: Session, feedback: schemas.FeedbackBase):
    """Create feedback in db"""
    db_feedback = Feedback(content=feedback.content)
    commit_changes_to_object(database=database, obj=db_feedback)
    return db_feedback
