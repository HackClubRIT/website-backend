"""
Common utils for user Module
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from app.dependancies import SECRET_KEY, JWT_HASH_ALGORITHM
from .crud import get_user_by_username, verify_password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT Token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_HASH_ALGORITHM)
    return encoded_jwt


def authenticate_user(database, username, password):
    """Using username and password"""
    user = get_user_by_username(database, username)
    if user and verify_password(user, password):
        return user
    return None
