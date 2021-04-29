"""
Run server
"""
from fastapi import FastAPI

from .commons.mock_middleware import is_debug
from .users.endpoints import router as user_router
from .applications.endpoints import router as application_router
from .settings import DEBUG

# Disable Docs in Production
if DEBUG:
    DOCS_URL = "/docs"
else:
    DOCS_URL = None

app = FastAPI(docs_url=DOCS_URL)
app.include_router(user_router)
app.include_router(application_router)


@app.get("/")
def test():
    """Test route"""
    is_debug()
    return "Hello World"
