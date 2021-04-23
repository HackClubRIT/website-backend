from enum import Enum


class Roles(Enum):
    """The role enum"""
    admin = "admin"
    moderator = "moderator"
    user = "user"


hierarchy = {
    Roles.admin: 0,
    Roles.moderator: 1,
    Roles.user: 2
}
