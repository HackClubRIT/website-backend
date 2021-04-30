"""
Test user module
"""
from fastapi.testclient import TestClient
from app.main import app
from app.database.config_db import Base
from app.database.config_test_db import engine

client = TestClient(app)


