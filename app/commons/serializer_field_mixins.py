"""
Common Validators
"""
# pylint: disable=no-self-argument,no-self-use
import re

from pydantic import BaseModel, validator


def _name_validator(name):
    """Letters and Whitespaces allowed"""
    pattern = r"^[A-Za-z \.]+$"
    return re.search(pattern, name)


def _email_validator(email):
    """Email validate"""
    pattern = r'^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))' \
              r'@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])' \
              r'|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    return re.search(pattern, email)


class EmailMixin(BaseModel):
    """Email Field Mixin"""
    email: str

    @validator("email")
    def is_valid_email(cls, email):
        """Validate email if it exists"""
        if email:
            if not _email_validator(email):
                raise ValueError("Invalid Email")
        return email


class NameMixin(BaseModel):
    """Name field mixin"""
    name: str

    @validator("name")
    def is_valid_name(cls, name):
        """Validate name if it exists"""
        if name:
            if not _name_validator(name):
                raise ValueError("Invalid Name")
        return name
