from sqlalchemy.orm import Session
from app.database.database import commit_changes_to_object
from .models import Feedback
from . import schemas


def get_all_feedback(database: Session):
    return database.query(Feedback).order_by(Feedback.datetime.desc()).all()

def get_feedback_by_id(database: Session, unique_id: int):
    return database.query(Feedback).filter(Feedback.id == unique_id).first()

def create_feedback(database: Session, feedback: schemas.FeedbackBase):
    db_feedback = Feedback(content=feedback.content)
    commit_changes_to_object(database=database, obj=db_feedback)
    return db_feedback

