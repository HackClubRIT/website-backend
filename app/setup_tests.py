from app.database.config_db import Base
from app.database.config_test_db import engine
from app.main import app
from dependancies import get_test_db, get_db

# Create all tables
Base.metadata.create_all(bind=engine)

# Override db dependency
app.dependency_overrides[get_db] = get_test_db
