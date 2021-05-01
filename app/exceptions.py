"""
Standard responses for HTTPExceptions
"""
from fastapi import HTTPException

INTERNAL_SERVER_ERROR = "Something is wrong please try again later"

USER_FORBIDDEN = "You don't have the required permissions to perform this action"


class ValidationError(HTTPException):
    """Override HttpException for ValidationError"""
    def __init__(self, detail):
        super(ValidationError, self).__init__(detail=detail, status_code=422)
