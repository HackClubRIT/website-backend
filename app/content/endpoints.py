from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependancies import get_current_user, get_db
from app.users.roles import Roles
from app.users.schemas import UserInDB
from app.users.role_mock_middleware import is_at_least_role
from . import crud
from .schemas import FeedbackBase, FeedbackRead

router = APIRouter(
    prefix="/content",
    tags=["Content"],
)

@router.get("/feedback", response_model=List[FeedbackRead])
async def get_all_feedback(database: Session = Depends(get_db),
                     current_user: UserInDB = Depends(get_current_user)):
    """List all feedback data"""
    is_at_least_role(Roles.MODERATOR, current_user)
    return crud.get_all_feedback(database)

@router.get("/feedback/{feedback_id}", response_model=FeedbackRead)
async def get_feedback_by_id(feedback_id: int, database: Session = Depends(get_db),
                     current_user: UserInDB = Depends(get_current_user)):
    """Get feedback by id"""
    is_at_least_role(Roles.MODERATOR, current_user)
    return crud.get_feedback_by_id(database, feedback_id)

@router.post("/feedback", response_model=FeedbackRead)
async def create_feedback(feedback: FeedbackBase, database: Session = Depends(get_db)):
    """Create feedback"""
    return crud.create_feedback(database, feedback)