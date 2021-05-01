"""
Test user module
"""
from fastapi.testclient import TestClient
from app.setup_tests import set_up, set_up_users, DEFAULT_PASSWORD, set_auth
from app.main import app
from app.users.schemas import Token

client = TestClient(app)

set_up()

USERS = set_up_users()


def test_get_user():
    for role, user in USERS.items():
        response = client.get("/auth/user/%d" % user.id)
        assert response.status_code == 200


def test_login_and_token():
    for role, user in USERS.items():
        response = client.post("/auth/token", data={"username": user.email, "password": DEFAULT_PASSWORD})
        assert response.status_code == 200
        token = Token(**response.json())
        response = client.get("/auth/check", headers=set_auth(token))
        assert response.status_code == 204

