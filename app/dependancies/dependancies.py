"""
Common methods
"""
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.users.schemas import TokenData, UserInDB
from app.database import SessionLocal
from app.users.crud import get_user_by_username

JWT_HASH_ALGORITHM = "HS256"

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

SECRET_KEY = os.environ.get("SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_db():
    """
    Get the current db session
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


def get_current_user(database: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    :return: schemas.UserInDB
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_HASH_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as jwt_exception:
        raise credentials_exception from jwt_exception
    user = get_user_by_username(database=database, username=token_data.username)
    if user is None:
        raise credentials_exception
    return UserInDB(**user.__dict__)
