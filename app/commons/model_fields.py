"""
Common model fields
"""
from datetime import datetime
from dateutil.tz import gettz
from sqlalchemy import TypeDecorator, DateTime
from app.settings import TZ


class AwareDateTime(TypeDecorator):
    # pylint: disable=abstract-method
    """Custom field to handle timezones"""

    cache_ok = False

    @property
    def python_type(self):
        """python type"""
        return datetime

    impl = DateTime

    def process_bind_param(self, value, dialect):
        """Convert to UTC time before saving"""
        if value.tzinfo is None:
            # Set native timezone objects to default TZ
            value = value.replace(tzinfo=gettz(TZ))
        return value

    def process_result_value(self, value, dialect):
        """Convert to TZ after fetching as UTC from DB"""
        return value.replace(tzinfo=gettz(TZ))
