"""
App Settings
"""

import os

DEBUG = os.environ.get("DEBUG", "True") != "False"

JWT_HASH_ALGORITHM = "HS256"

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

SECRET_KEY = os.environ.get("SECRET_KEY")
