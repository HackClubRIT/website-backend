"""
App Settings
Django inspired settings file
"""
import json
import os
from fastapi_mail import ConnectionConfig, FastMail

DEBUG = os.environ.get("DEBUG", "true") != "false"

JWT_HASH_ALGORITHM = "HS256"

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

SECRET_KEY = os.environ.get("SECRET_KEY",
                            "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")

ALLOWED_ORIGINS = json.loads(os.environ.get("ALLOWED_ORIGINS", "[]"))
print(ALLOWED_ORIGINS)
_EMAIL_CONF = ConnectionConfig(
    MAIL_USERNAME=os.environ.get("EMAIL_USERNAME", ""),
    MAIL_PASSWORD=os.environ.get("EMAIL_PASSWORD", ""),
    MAIL_FROM=os.environ.get("EMAIL_FROM", "test@test.com"),
    MAIL_PORT=int(os.environ.get("EMAIL_PORT", 0)),
    MAIL_SERVER=os.environ.get("EMAIL_SERVER", ""),
    MAIL_TLS=os.environ.get("EMAIL_TLS", "false") != "false",
    MAIL_SSL=os.environ.get("EMAIL_SSL", "false") != "false",
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="./app/emails"
)

fastapi_mail_instance = FastMail(_EMAIL_CONF)

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
