"""
Common Validators
"""
import re


def name_validator(name):
    """Letters and Whitespaces allowed"""
    pattern = r"^[A-Za-z ]+$"
    return re.search(pattern, name)


def email_validator(email):
    """Email validate"""
    pattern = r'^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))' \
              r'@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])' \
              r'|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    return re.search(pattern, email)
