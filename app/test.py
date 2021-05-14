"""
Test Utils
"""
from abc import abstractmethod
from random import randint
from fastapi.testclient import TestClient
from app.database.config_db import Base
from app.database.config_test_db import engine
from app.main import app
from app.dependancies import get_test_db, get_db
from app.users.roles import Roles
from .settings import fastapi_mail_instance
from .users.crud import create_user
from .users.schemas import UserCreate, User, Token


class FeatureTest:
    """
    The TestInstance Class contains all utilities for running tests
    """
    def __init__(self, database, **kwargs):
        """
        Pre test Setup
        """
        # Refresh test db
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        # Override db dependency
        app.dependency_overrides[get_db] = get_test_db

        # Dont send mail
        fastapi_mail_instance.config.SUPPRESS_SEND = 1

        self.client = TestClient(app)
        self.mail_instance = fastapi_mail_instance
        self.users = {}
        self.database_conn = database
        self.default_password = FeatureTest.random_string(randint(8, 20))
        self.set_up_users()
        self.additional_setup(**kwargs)

    def set_up_users(self):
        """Create a user for each role and save to self.users"""
        for role in Roles:
            self.users[role] = UserCreate(
                name=FeatureTest.random_string(),
                # Ensure unique email
                email=role.value+self.random_email(),
                password=self.default_password,
                role=role
            )
            db_user = create_user(self.database_conn, user=self.users[role])
            #response = self.client.post("/auth/user", data=self.users[role].json())
            #assert response.status_code == 201
            self.users[role] = User(**db_user.__dict__)

    @abstractmethod
    def additional_setup(self, **kwargs):
        """Override this to create other objects for testing"""

    def set_auth_from_user(self, user):
        """
        Shortcut fn to directly set header from user
        """
        return self.set_auth(self.get_token(user))

    def get_token(self, user):
        """
        :returns users.schema.Token
        """
        data = {"email": user.email, "password": self.default_password}
        response = self.client.post("/auth/token", json=data)
        print(response.__dict__)
        print(response.status_code)
        assert response.status_code == 200
        return Token(**response.json())

    @staticmethod
    def random_string(length=10, assure_num=False):
        """
        assure_num: When true string will contain a numeric value too
        """
        string = "".join([chr(randint(65, 90)) for _ in range(length)])
        if assure_num:
            return string + "1"
        return string

    @staticmethod
    def random_email():
        """Random Email"""
        return FeatureTest.random_string().lower() + "@somedomain.com"

    @staticmethod
    def set_auth(token: Token):
        """Set Authorization Header"""
        return {
            "Authorization": "%s %s" % (
                token.token_type.capitalize(),
                token.access_token
            )
        }
