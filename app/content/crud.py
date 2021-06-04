"""
CRUD Feedbacks, Events
"""
import pytz
from datetime import datetime
from sqlalchemy.orm import Session
from app.database.database import commit_changes_to_object, update_instance
from app.settings import TZ
from .models import Feedback, Event
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


def get_all_events(database: Session):
    """Get events from database"""
    return database.query(Event).order_by(Event.date.desc()).all()


def get_upcoming_events(database: Session):
    """Get upcoming events"""
    return database.query(Event).filter(Event.date >= datetime.now(pytz.timezone(TZ)))


def get_event_by_id(database: Session, event_id: int):
    """Get event by id"""
    return database.query(Event).filter(Event.id == event_id)


def create_event(database: Session, event: schemas.EventBaseSerializer, current_user):
    """Create Event"""
    db_event = Event(**event.json())
    db_event.user_id = current_user.id
    commit_changes_to_object(database=database, obj=db_event)
    return db_event


def add_image_link_to_event(database: Session, image_url: str, event_id: int,
                            db_event: Event = None):
    """Add image to event"""
    if db_event is None:
        db_event = get_event_by_id(database, event_id)
    db_event.image_url = image_url
    commit_changes_to_object(database=database, obj=db_event)
    return db_event


def update_event_data(database: Session, event_id: int,
                      event_updated: schemas.EventUpdateSerializer, db_event: Event = None):
    """Update event data except image"""
    if db_event is None:
        db_event = get_event_by_id(database, event_id)

    update_instance(database, db_event, event_updated)
    return db_event


def delete_event(database: Session, event_id: int, db_event: Event = None):
    """Delete event from db"""
    if db_event is None:
        db_event = get_event_by_id(database, event_id)
    database.delete(db_event)
    commit_changes_to_object(database, db_event)
