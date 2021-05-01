from app.database.config_db import Base
from app.database.config_test_db import engine
from app.main import app
from app.dependancies import get_test_db, get_db
from app.users.roles import Roles
from .users.schemas import UserCreate, User, Token
from fastapi.testclient import TestClient

DEFAULT_PASSWORD = "password"


def set_auth(token: Token):
    """Set Authorization Header"""
    return {
        "Authorization": "%s %s" % (
            token.token_type.capitalize(),
            token.access_token
        )
    }


def set_up():
    # Create all tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Override db dependency
    app.dependency_overrides[get_db] = get_test_db


def set_up_users():
    """Create a user for each role and return them"""
    client = TestClient(app)
    users = {
        Roles.ADMIN: UserCreate(
            name="ADMIN",
            role=Roles.ADMIN,
            email="admin@abcd.com",
            password=DEFAULT_PASSWORD
        ),
        Roles.MODERATOR: UserCreate(
            name="MOD",
            role=Roles.MODERATOR,
            email="mod@abcd.com",
            password=DEFAULT_PASSWORD
        ),
        Roles.USER: UserCreate(
            name="USER",
            role=Roles.USER,
            email="user@abcd.com",
            password=DEFAULT_PASSWORD
        ),
    }

    for role, user in users.items():
        response = client.post("/auth/user", data=user.json())
        assert response.status_code == 201
        users[role] = User(**response.json())

    return users
