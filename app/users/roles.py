from enum import Enum


class Roles(Enum):
    """
    The role enum
    WARNING: Don't change values unnecessarily as this enum is directly tied to migration '0979a70968e5'
    """
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    USER = "USER"


hierarchy = {
    Roles.ADMIN: 2,
    Roles.MODERATOR: 1,
    Roles.USER: 0
}
