"""
Run server
"""
from fastapi import FastAPI
from .commons.mock_middleware import is_debug
from .users.endpoints import router as user_router
from .applications.endpoints import router as application_router
from .settings import get_docs_url, get_origin_settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    docs_url=get_docs_url(),
)

app.add_middleware(
    CORSMiddleware,
    **get_origin_settings()
)

app.include_router(user_router)
app.include_router(application_router)


@app.get("/")
def test():
    """Test route"""
    is_debug()
    return "Hello World"
