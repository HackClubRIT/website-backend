"""
Run server
"""
from fastapi import FastAPI
from .users.endpoints import router as user_router
from .applications.endpoints import router as application_router

app = FastAPI()
app.include_router(user_router)
app.include_router(application_router)


@app.get("/")
def test():
    """Test route"""
    return "Hello World"
