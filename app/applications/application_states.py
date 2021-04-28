# pylint: disable=missing-module-docstring
from enum import Enum


class ApplicationStates(Enum):
    """
    ApplicationStates Enum
    """
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
