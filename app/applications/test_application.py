"""
Application Tests
"""
import json
from random import randint
import pytest
from app.applications.schemas import ApplicationRead
from app.test import FeatureTest
from app.users.roles import Roles
# pytest needs the fixture to be same name
# pylint: disable=redefined-outer-name

USER_READ_PERMISSIONS = {
    Roles.ADMIN: 200,
    Roles.MODERATOR: 200,
    Roles.USER: 403,
}


class ApplicationTest(FeatureTest):
    """
    Setup Application Tests
    """
    def __init__(self):
        self.applications = []
        super().__init__()

    def new_application(self, invalid_name=False, invalid_email=False):
        """
        Create new Application with Endpoint
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

            response = self.client.post("/application/", data=json.dumps(new_application))
            assert response.status_code == 201
            self.applications.append(ApplicationRead(**response.json()))


@pytest.fixture
def test_instance():
    """Yield a new instance of ApplicationTest everytime a test runs"""
    yield ApplicationTest()


def assert_user_permissions(test_instance, users, url, method="GET", data=None, json_=None):
    """
    Test the same endpoint using different credentials
    :param test_instance: The Current FeatureTest
    :param users: Dict containing users and expected status codes
    :param url: Endpoint
    :param method: The request method
    :param data: data of client.request
    :param json_: json of client.request
    """
    methods = {
        "GET": test_instance.client.get,
        "PATCH": test_instance.client.patch,
        "POST": test_instance.client.post
    }
    for user, status_code in users.items():
        response = methods[method](
            url,
            data=data,
            json=json_,
            headers=test_instance.set_auth_from_user(test_instance.users[user])
        )
        assert response.status_code == status_code


def test_view_all_applications(test_instance):
    """
    TEST GET /application
    """
    # Unauthenticated
    response = test_instance.client.get("/application")
    assert response.status_code == 401

    assert_user_permissions(
        test_instance,
        USER_READ_PERMISSIONS,
        "/application"
    )


def test_view_application(test_instance):
    """
    TEST GET /application/{application.id}
    """

    for application in test_instance.applications:
        # Unauthenticated
        response = test_instance.client.get("/application/%d" % application.id)
        assert response.status_code == 401

        assert_user_permissions(
            test_instance,
            USER_READ_PERMISSIONS,
            url="/application/%d" % application.id,
        )


def test_create_application_fail(test_instance):
    """
    TEST POST /application
    Success case is actually tested when fixtures is ran, So test only fail cases
    """
    response = test_instance.client.post(
        "/application/",
        data=json.dumps(test_instance.new_application(invalid_name=True))
    )
    assert response.status_code == 422

    response = test_instance.client.post(
        "/application/",
        data=json.dumps(test_instance.new_application(invalid_email=True))
    )
    assert response.status_code == 422


def test_update_application(test_instance):
    """
    TEST PATCH /application/{application.id}
    """
    application = test_instance.applications[0]
    # Unauthenticated
    response = test_instance.client.patch(
        "/application/%d" % application.id
    )
    assert response.status_code == 401
    # Not Acceptable
    response = test_instance.client.patch(
        "/application/%d" % application.id,
        json={"approved": "ACCEPTED"},
        headers=test_instance.set_auth_from_user(test_instance.users[Roles.ADMIN])
    )
    assert response.status_code == 422
    # Admin approved
    application = test_instance.applications[1]
    response = test_instance.client.patch(
        "/application/%d" % application.id,
        json={"approved": True},
        headers=test_instance.set_auth_from_user(test_instance.users[Roles.ADMIN])
    )
    assert response.status_code == 200
    # Admin reject
    application = test_instance.applications[2]
    response = test_instance.client.patch(
        "/application/%d" % application.id,
        json={"approved": False},
        headers=test_instance.set_auth_from_user(test_instance.users[Roles.ADMIN])
    )
    assert response.status_code == 200
    # Admin approves rejected application
    response = test_instance.client.patch(
        "/application/%d" % application.id,
        json={"approved": True},
        headers=test_instance.set_auth_from_user(test_instance.users[Roles.ADMIN])
    )
    assert response.status_code == 400
    # Other users try updating
    users = {
        Roles.MODERATOR: 403,
        Roles.USER: 403
    }
    for application in test_instance.applications[3:]:
        assert_user_permissions(
            test_instance,
            users,
            method="PATCH",
            url="/application/%d" % application.id,
            json_={"approved": randint(0, 9) > 4}
        )
