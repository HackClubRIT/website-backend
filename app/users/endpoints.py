"""
The endpoints for /user
"""
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.dependancies import get_db
from . import crud
from .schemas import User, UserWrite

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, database: Session = Depends(get_db)):
    """Get user by ID"""
    db_user = crud.get_user(database=database, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=User)
async def create_user(user: UserWrite, database: Session = Depends(get_db)):
    """Create a new user"""
    existing_user = crud.get_user_by_username(database=database, username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    return crud.create_user(user=user, database=database)


@router.get("/login")
def login(user: UserWrite, database: Session = Depends(get_db)):
    """Login"""
    pass
