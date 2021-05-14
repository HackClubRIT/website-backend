"""
The endpoints for /auth
"""
from datetime import timedelta
from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.exceptions import USER_FORBIDDEN
from app.dependancies import get_db, get_current_user
from app.settings import JWT_ACCESS_TOKEN_EXPIRE_MINUTES
from app.commons.mock_middleware import is_debug
from . import crud
from .role_mock_middleware import is_admin
from .schemas import User, UserCreate, Token, UserUpdate, UserInDB, UserLogin
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
    is_debug(status_code=405)
    existing_user = crud.get_user_by_email(
        database=database,
        email=user.email,
        all_users=True
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    return crud.create_user(user=user, database=database)


@router.patch("/user/{user_id}", response_model=User)
def update_user_partial(user_id: int, new_user_data: UserUpdate,
                        current_user: UserInDB = Depends(get_current_user),
                        database: Session = Depends(get_db)):
    """Update User EndPoint"""
    if current_user.id == user_id or is_admin(current_user):

        if hasattr(new_user_data, "email"):
            same_email_user = crud.get_user_by_email(
                database=database,
                email=new_user_data.email,
                all_users=True
            )
            if same_email_user and same_email_user.id != user_id:
                # Verify that there really exists another user with the same email
                raise HTTPException(status_code=400, detail="Username already taken")

        new_user_from_db = crud.update_user(
            database=database,
            user_updated=new_user_data,
            user_id=user_id
        )

        if new_user_from_db:
            return new_user_from_db
        raise HTTPException(status_code=400, detail="User Not Found")
    raise HTTPException(status_code=403, detail=USER_FORBIDDEN)


@router.delete("/user/{user_id}", status_code=204)
def delete_user(user_id: int,
                current_user: UserInDB = Depends(get_current_user),
                database: Session = Depends(get_db)):
    """Delete User Endpoint"""

    if current_user.id != user_id and not is_admin(current_user):
        raise HTTPException(status_code=403, detail=USER_FORBIDDEN)
    if not crud.delete_user(database, user_id):
        # If the current user is not in db
        raise HTTPException(status_code=400, detail="User not found")


@router.post("/token", response_model=Token)
def login_for_access_token(login_data: UserLogin, database: Session = Depends(get_db)):
    """Login Via email, password to get token"""
    user = authenticate_user(database, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/check", status_code=204)
def is_authenticated(_: UserInDB = Depends(get_current_user)):
    """Check Auth"""
    return None
