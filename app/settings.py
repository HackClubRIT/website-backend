"""
App Settings
"""
import json

from fastapi.middleware.cors import CORSMiddleware
import os

DEBUG = os.environ.get("DEBUG", "True") != "False"

JWT_HASH_ALGORITHM = "HS256"

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_ORIGINS = json.loads(os.environ.get("ALLOWED_ORIGINS", "[]"))

assert type(ALLOWED_ORIGINS) is list


def get_origin_settings():
    """Set CORS Settings According To DEBUG"""
    settings = {
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"]
    }

    if DEBUG:
        settings["allow_origins"] = ["*"]
    else:
        settings["allow_origins"] = ALLOWED_ORIGINS

    return settings


def get_docs_url():
    """Set docs url according to DEBUG"""
    # Disable Docs in Production
    if DEBUG:
        return "/docs"
    return None
