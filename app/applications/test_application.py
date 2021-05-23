"""
Application Tests
"""
import json
from random import randint
from app.applications.schemas import ApplicationRead, ApplicationBase
from app.users.crud import get_user_by_email
from app.test import FeatureTest
from app.users.roles import Roles
from .crud import create_application


USER_READ_PERMISSIONS = {
    Roles.ADMIN: 200,
    Roles.MODERATOR: 200,
    Roles.USER: 403,
}


class ApplicationTest(FeatureTest):
    """
    Setup Application Tests
    """
    def __init__(self, database):
        self.applications = []
        super().__init__(database)

    def new_application(self, invalid_name=False, invalid_email=False):
        """
        Create new Application Object
        """
        data = {
            "email": self.random_email(),
            "name": self.random_string(),
            "data": {
                self.random_string(): self.random_string()
            }
        }
        if invalid_name:
            data["name"] += "1"
        if invalid_email:
            data["email"] = self.random_string()
        return data

    def additional_setup(self, **kwargs):
        for _ in range(5):
            new_application = self.new_application()
            db_application = create_application(
                self.database_conn, ApplicationBase(**new_application)
            )
            self.applications.append(ApplicationRead(**db_application.__dict__))


def test_view_all_applications(test_application_instance):
    """
    TEST GET /application
    """
    # Unauthenticated
    response = test_application_instance.client.get("/application")
    assert response.status_code == 401

    test_application_instance.assert_user_permissions(
        USER_READ_PERMISSIONS,
        "/application"
    )


def test_view_application(test_application_instance):
    """
    TEST GET /application/{application.id}
    """

    for application in test_application_instance.applications:
        # Unauthenticated
        response = test_application_instance.client.get("/application/%d" % application.id)
        assert response.status_code == 401

        test_application_instance.assert_user_permissions(
            USER_READ_PERMISSIONS,
            url="/application/%d" % application.id,
        )


def test_create_application_fail(test_application_instance):
    """
    TEST POST /application
    Success case is actually tested when fixtures is ran, So test only fail cases
    """
    response = test_application_instance.client.post(
        "/application/",
        data=json.dumps(test_application_instance.new_application(invalid_name=True))
    )
    assert response.status_code == 422

    response = test_application_instance.client.post(
        "/application/",
        data=json.dumps(test_application_instance.new_application(invalid_email=True))
    )
    assert response.status_code == 422


def test_update_application(test_application_instance):
    """
    TEST PATCH /application/{application.id}
    """
    application = test_application_instance.applications[0]
    # Unauthenticated
    response = test_application_instance.client.patch(
        "/application/%d" % application.id
    )
    assert response.status_code == 401
    # Not Acceptable
    response = test_application_instance.client.patch(
        "/application/%d" % application.id,
        json={"approved": "ACCEPTED"},
        headers=test_application_instance.
            set_auth_from_user(test_application_instance.users[Roles.ADMIN])
    )
    assert response.status_code == 422
    # Admin approved
    with test_application_instance.mail_instance.record_messages() as outbox:
        application = test_application_instance.applications[1]
        response = test_application_instance.client.patch(
            "/application/%d" % application.id,
            json={"approved": True},
            headers=test_application_instance.
                set_auth_from_user(test_application_instance.users[Roles.ADMIN])
        )
        assert response.status_code == 200
        # Test User Creation
        assert get_user_by_email(
            database=test_application_instance.database_conn,
            email=application.email) is not None
        # Check mail
        assert len(outbox) == 1
        outbox.pop()

        # Admin reject
        application = test_application_instance.applications[2]
        response = test_application_instance.client.patch(
            "/application/%d" % application.id,
            json={"approved": False},
            headers=test_application_instance.
                set_auth_from_user(test_application_instance.users[Roles.ADMIN])
        )
        assert response.status_code == 200
        # Check mail
        assert len(outbox) == 1

    # Admin approves rejected application
    response = test_application_instance.client.patch(
        "/application/%d" % application.id,
        json={"approved": True},
        headers=test_application_instance.
            set_auth_from_user(test_application_instance.users[Roles.ADMIN])
    )
    assert response.status_code == 400
    # Other users try updating
    users = {
        Roles.MODERATOR: 403,
        Roles.USER: 403
    }
    for application in test_application_instance.applications[3:]:
        test_application_instance.assert_user_permissions(
            users,
            method="PATCH",
            url="/application/%d" % application.id,
            json_={"approved": randint(0, 9) > 4}
        )
