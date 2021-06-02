"""
Test Feedback Feature
"""
from app.test import FeatureTest
from app.users.roles import Roles
from .crud import create_feedback, get_feedback_by_id
from .schemas import FeedbackBase


class FeedbackTest(FeatureTest):
    """
    Utilities for feedback tests
    """
    def __init__(self, database):
        self.feedbacks = []
        super().__init__(database)

    def additional_setup(self, **kwargs):
        for _ in range(5):
            self.feedbacks.append(
                create_feedback(
                    self.database_conn,
                    FeedbackBase(content=self.random_string())
                )
            )


USER_READ_FEEDBACK_STATUS_CODE = {
    Roles.ADMIN: 200,
    Roles.MODERATOR: 200,
    Roles.USER: 403
}


def test_get_all_feedbacks(test_feedback_instance: FeedbackTest):
    """
    TEST GET /content/feedback
    """
    test_feedback_instance.assert_user_permissions(
        USER_READ_FEEDBACK_STATUS_CODE,
        "/content/feedback/",
    )


def test_get_application_by_id(test_feedback_instance: FeedbackTest):
    """
    TEST GET /content/feedback/{id}
    """
    for feedback in test_feedback_instance.feedbacks:
        test_feedback_instance.assert_user_permissions(
            USER_READ_FEEDBACK_STATUS_CODE,
            "/content/feedback/%d/" % feedback.id,
        )


def test_create_application(test_feedback_instance: FeedbackTest):
    """
    TEST POST /content/feedback
    """
    feedback = FeedbackBase(content=test_feedback_instance.random_string())
    response = test_feedback_instance.client.post(
        "/content/feedback/",
        data=feedback.json(),
    )
    assert response.status_code == 201
    feedback_id = response.json()["id"]
    assert get_feedback_by_id(
        test_feedback_instance.database_conn, feedback_id) is not None
