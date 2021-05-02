"""
App Settings
Django inspired settings file
"""
import json
import os

DEBUG = os.environ.get("DEBUG", "true") != "false"

JWT_HASH_ALGORITHM = "HS256"

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_ORIGINS = json.loads(os.environ.get("ALLOWED_ORIGINS", "[]"))

TZ = "Asia/Calcutta"

assert isinstance(ALLOWED_ORIGINS, list)


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
