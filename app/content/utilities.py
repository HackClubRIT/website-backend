from fastapi import HTTPException
from app.content.crud import get_event_by_id
from app.exceptions import USER_FORBIDDEN
from app.users.role_mock_middleware import is_at_least_role
from app.users.roles import Roles


def verify_user_permissions_to_update_event(user, event_id, database):
    """
    :param user: User Object, intended as logged in user
    :param event_id: Event Id
    :param database: database session
    """
    is_at_least_role(Roles.MODERATOR, user)
    db_event = get_event_by_id(database, event_id)
    if db_event.user_id != user.id and user.role != Roles.ADMIN:
        raise HTTPException(
            status_code=403,
            detail=USER_FORBIDDEN)

    return db_event
