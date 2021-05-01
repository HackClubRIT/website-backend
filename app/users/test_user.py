"""
Test user module
"""
from random import randint
from app.test import TestInstance
from app.users.schemas import Token

test_instance = TestInstance()


def test_get_user():
    """Test GET /auth/user/:userId"""
    for role, user in test_instance.users.items():
        response = test_instance.client.get("/auth/user/%d" % user.id)
        assert response.status_code == 200


def test_login_and_token_fail():
    """Test POST /auth/user Fail Case"""
    for role, user in test_instance.users.items():
        response = test_instance.client.post(
            "/auth/token",
            data={
                "username": user.email,
                "password": test_instance.default_password + chr(randint(65, 90))
            }
        )
        assert response.status_code == 401


def test_login_and_token_success():
    """Test POST /auth/user Success Case"""
    for role, user in test_instance.users.items():
        login_data = {"username": user.email, "password": test_instance.default_password}
        response = test_instance.client.post("/auth/token", data=login_data)
        assert response.status_code == 200
        token = Token(**response.json())
        response = test_instance.client.get("/auth/check", headers=test_instance.set_auth(token))
        assert response.status_code == 204


def test_partial_update_invalid_data():
    """
    Test PATCH /auth/user/:userId
    Only with invalid data
    """
    invalid_name_and_email = "".join([chr(randint(65, 90))+str(i) for i in range(randint(4, 10))])
    invalid_password = "".join([chr(randint(65, 90)) for i in range(randint(0, 7))])
    for role, user in test_instance.users.items():
        response = test_instance.client.patch(
            "/auth/user/%d" % user.id,
            data={"email": invalid_name_and_email},
        )
        assert response.status_code == 422
        response = test_instance.client.patch(
            "/auth/user/%d" % user.id,
            data={"name": invalid_name_and_email},
        )
        assert response.status_code == 422
        response = test_instance.client.patch(
            "/auth/user/%d" % user.id,
            data={"password": invalid_password},
        )
        assert response.status_code == 422


def test_partial_update_invalid_permissions():
    """
    Test PATCH /auth/user/:userId
    Invalid permissions
    """
    pass
