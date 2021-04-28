"""
fastAPI doesn't allow each route to define its middlewares yet.
So as of now these are 'mock' middlewares, expected to mimic the behaviour of middlewares until this
feature is implemented in fastAPI
"""
from fastapi import HTTPException
from app.exception_response_body import USER_FORBIDDEN
from .roles import Roles, hierarchy

exception = HTTPException(status_code=403, detail=USER_FORBIDDEN)


def is_role(role: Roles, current_user):
    """
    Check if current_user.role == role
    :raises HTTPException 403 otherwise
    """
    if current_user.role != role:
        raise exception
    return True


def is_at_least_role(role: Roles, current_user):
    """
    Check if current_user.role >= role in the hierarchy
    :raises HTTPException 403 otherwise
    """
    if hierarchy.get(current_user.role) < hierarchy.get(role):
        raise exception
    return True


def is_admin(current_user):
    """Checks if current user is admin"""
    return is_role(current_user=current_user, role=Roles.ADMIN)
