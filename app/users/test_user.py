"""
Test user module
"""
from random import randint
from app.test import TestInstance
from app.users.roles import Roles
test_instance = TestInstance()


def test_get_user():
    """Test GET /auth/user/:userId"""
    for _, user in test_instance.users.items():
        response = test_instance.client.get("/auth/user/%d" % user.id)
        assert response.status_code == 200


def test_login_and_token_fail():
    """Test POST /auth/user Fail Case"""
    for _, user in test_instance.users.items():
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
    for _, user in test_instance.users.items():
        token = test_instance.get_token(user)
        response = test_instance.client.get("/auth/check", headers=test_instance.set_auth(token))
        assert response.status_code == 204


def test_partial_update_invalid_data():
    """
    Test PATCH /auth/user/:userId
    Only with invalid data
    """
    invalid_name_and_email = test_instance.random_string(assure_num=True)
    invalid_password = test_instance.random_string(randint(1, 7))
    invalid_datas = [
        {"email": invalid_name_and_email},
        {"name": invalid_name_and_email},
        {"password": invalid_password}
    ]
    for _, user in test_instance.users.items():
        for invalid_data in invalid_datas:
            response = test_instance.client.patch(
                "/auth/user/%d" % user.id,
                json=invalid_data,
                headers=test_instance.set_auth(test_instance.get_token(user))
            )
            assert response.status_code == 422


def test_partial_update_invalid_permissions():
    """
    Test PATCH /auth/user/:userId
    Invalid permissions
    """
    non_auth_users = [user for role, user in test_instance.users.items() if role != Roles.ADMIN]
    for current_user in non_auth_users:
        other_users = [user for _, user in test_instance.users.items() if user != current_user]

        token = test_instance.get_token(current_user)
        for user in other_users:
            email = test_instance.random_email()
            response = test_instance.client.patch(
                "/auth/user/%d" % user.id,
                headers=test_instance.set_auth(token),
                json={"email": email}
            )
            assert response.status_code == 403


def test_partial_update_success():
    """
    Test PATCH /auth/user/:userId
    Success Case
    """
    admin_user = test_instance.users[Roles.ADMIN]
    for _, user in test_instance.users.items():
        # Admin Update
        response = test_instance.client.patch(
            "/auth/user/%d" % user.id,
            headers=test_instance.set_auth(test_instance.get_token(admin_user)),
            json={"name": test_instance.random_string()}
        )
        assert response.status_code == 200
        # Self Update
        response = test_instance.client.patch(
            "/auth/user/%d" % user.id,
            headers=test_instance.set_auth(test_instance.get_token(user)),
            json={"name": test_instance.random_string()}
        )
        assert response.status_code == 200


def test_delete():
    """
    Test DELETE /auth/user/:userId
    Success Case
    """
    admin_user = test_instance.users[Roles.ADMIN]
    mod_user = test_instance.users[Roles.MODERATOR]
    normal_user = test_instance.users[Roles.USER]

    # Test if admin can delete any user
    response = test_instance.client.delete(
        "/auth/user/%d" % normal_user.id,
        headers=test_instance.set_auth(test_instance.get_token(admin_user))
    )
    assert response.status_code == 204
    response = test_instance.client.get("/auth/user/%d" % normal_user.id)
    assert response.status_code == 404

    # Test if a user can delete itself
    response = test_instance.client.delete(
        "/auth/user/%d" % mod_user.id,
        headers=test_instance.set_auth(test_instance.get_token(mod_user))
    )
    assert response.status_code == 204
    response = test_instance.client.get("/auth/user/%d" % mod_user.id)
    assert response.status_code == 404
