"""
Common Mock Middlewares
"""
from fastapi import HTTPException

from app.settings import DEBUG


def is_debug(status_code=404):
    """
    :param status_code: default - 404
    :raises HttpException with `status_code` if production
    """
    code_detail_map = {
        404: "Not found",
        405: "Method not allowed"
    }
    if not DEBUG:
        raise HTTPException(
            status_code=status_code,
            detail=code_detail_map[status_code]
        )
