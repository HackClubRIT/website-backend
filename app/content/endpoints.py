"""
Content Endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependancies import get_current_user, get_db
from app.users.roles import Roles
from app.users.schemas import UserInDB
from app.users.role_mock_middleware import is_at_least_role
from . import crud
from .schemas import FeedbackBase, FeedbackRead, EventReadSerializer, EventBaseSerializer, EventUpdateSerializer
from .utilities import verify_user_permissions_to_update_event
from ..exceptions import USER_FORBIDDEN

router = APIRouter(
    prefix="/content",
    tags=["Content"],
)


@router.get("/feedback/", response_model=List[FeedbackRead])
async def get_all_feedback(database: Session = Depends(get_db),
                           current_user: UserInDB = Depends(get_current_user)):
    """List all feedback data"""
    is_at_least_role(Roles.MODERATOR, current_user)
    return crud.get_all_feedback(database)


@router.get("/feedback/{feedback_id}/", response_model=FeedbackRead)
async def get_feedback_by_id(feedback_id: int, database: Session = Depends(get_db),
                             current_user: UserInDB = Depends(get_current_user)):
    """Get feedback by id"""
    is_at_least_role(Roles.MODERATOR, current_user)
    return crud.get_feedback_by_id(database, feedback_id)


@router.post("/feedback/", response_model=FeedbackRead, status_code=201)
async def create_feedback(feedback: FeedbackBase, database: Session = Depends(get_db)):
    """Create feedback"""
    return crud.create_feedback(database, feedback)


@router.get("/events/", response_model=List[EventReadSerializer])
def get_events(upcoming: str = "false", database: Session = Depends(get_db)):
    """List Events"""
    if upcoming == "true":
        return crud.get_upcoming_events(database)
    return crud.get_all_events(database)


@router.get("/events/{event_id}/", response_model=EventReadSerializer)
def get_event_by_id(event_id: int, database: Session = Depends(get_db)):
    """Retrieve Event By Id"""
    return crud.get_event_by_id(database, event_id)


@router.post("/events/", response_model=EventReadSerializer)
def create_event(event: EventBaseSerializer, user=Depends(get_current_user),
                 database: Session = Depends(get_db)):
    """Create event"""
    is_at_least_role(Roles.MODERATOR, user)
    return crud.create_event(database, event, user)


@router.patch("/events/{event_id}/image", response_model=EventReadSerializer)
def upload_image(event_id: int, user=Depends(get_current_user),
                 database: Session = Depends(get_db)):

    db_event = verify_user_permissions_to_update_event(
        event_id=event_id,
        database=database,
        user=user)

    # TODO Handle Image
    return db_event


@router.patch("/events/{event_id}/", response_model=EventReadSerializer)
def edit_non_image_event_data(event_id: int, event: EventUpdateSerializer,
                              user=Depends(get_current_user),
                              database: Session = Depends(get_db)):
    db_event = verify_user_permissions_to_update_event(
        event_id=event_id,
        database=database,
        user=user)

    return crud.update_event_data(database, event_id, event, db_event)


@router.delete("/events/{event_id}/", status_code=204)
def delete_event(event_id: int, user=Depends(get_current_user),
                 database: Session = Depends(get_db)):

    db_event = verify_user_permissions_to_update_event(
        event_id=event_id,
        database=database,
        user=user)

    crud.delete_event(database, event_id, db_event)

    # TODO Delete image
