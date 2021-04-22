"""
The endpoints for /user
"""
from datetime import timedelta
from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.openapi.models import Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.exception_response_body import INTERNAL_SERVER_ERROR, USER_FORBIDDEN
from app.dependancies import get_db, JWT_ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from . import crud
from .schemas import User, UserCreate, Token, UserUpdate, UserInDB
from .utils import authenticate_user, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


@router.get("/user/{user_id}", response_model=User)
def get_user(user_id: int, database: Session = Depends(get_db)):
    """Get user by ID"""
    db_user = crud.get_user(database=database, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/user", response_model=User, status_code=201)
def create_user(user: UserCreate, database: Session = Depends(get_db)):
    """Create a new user"""
    existing_user = crud.get_user_by_username(database=database, username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    return crud.create_user(user=user, database=database)


@router.patch("/user/{user_id}", response_model=User)
def update_user_partial(user_id: int, new_user_data: UserUpdate,
                        current_user: UserInDB = Depends(get_current_user),
                        database: Session = Depends(get_db)):
    """Update User EndPoint"""
    if current_user.id == user_id:
        if hasattr(new_user_data, "username") and \
                crud.get_user_by_username(database=database, username=new_user_data.username):
            raise HTTPException(status_code=400, detail="Username already taken")

        new_user_from_db = crud.update_user(database=database, user_updated=new_user_data, user_id=user_id)
        if new_user_from_db:
            return new_user_from_db
        # If the current user is not in db(For Some Reason)
        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR)
    raise HTTPException(status_code=403, detail=USER_FORBIDDEN)


@router.delete("/user/{user_id}", status_code=204)
def delete_user(user_id: int,
                current_user: UserInDB = Depends(get_current_user),
                database: Session = Depends(get_db)):
    """Delete User Endpoint"""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail=USER_FORBIDDEN)
    if not crud.delete_user(database, user_id):
        # If the current user is not in db(For Some Reason)
        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR)


@router.post("/token", response_model=Token)
def login_for_access_token(database: Session = Depends(get_db),
                           form_data: OAuth2PasswordRequestForm = Depends()):
    """Login Via username, password to get token"""
    user = authenticate_user(database, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
