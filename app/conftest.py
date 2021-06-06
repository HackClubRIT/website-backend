"""
The test fixtures
"""
import pytest
from app.applications.test_application import ApplicationTest
from app.content.test_event import EventTest
from app.database.config_test_db import TESTING_SESSION_LOCAL
from app.content.test_feedback import FeedbackTest
from app.test import FeatureTest


# pylint: disable=redefined-outer-name

@pytest.fixture(scope="module")
def db_fixture():
    """Yield a db session for testing"""
    db_conn = TESTING_SESSION_LOCAL()
    try:
        yield db_conn
    finally:
        db_conn.close()


@pytest.fixture(scope="module")
def test_instance(db_fixture):
    """Yield a new instance of FeatureTest everytime a new test module runs"""
    yield FeatureTest(db_fixture)


@pytest.fixture(scope="module")
def test_application_instance(db_fixture):
    """Yield a new instance of ApplicationTest everytime a new test module runs"""
    yield ApplicationTest(db_fixture)


@pytest.fixture(scope="module")
def test_feedback_instance(db_fixture):
    """Yield a new instance of FeedbackTest everytime a new test module runs"""
    yield FeedbackTest(db_fixture)


@pytest.fixture(scope="module")
def test_event_instance(db_fixture):
    """Yield a new instance of EventTest everytime a new test module runs"""
    yield EventTest(db_fixture)
