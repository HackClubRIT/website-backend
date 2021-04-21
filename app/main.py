"""
Run server
"""
from fastapi import FastAPI
from .users.endpoints import router as user_router

app = FastAPI()
app.include_router(user_router)


@app.get("/")
def test():
    """Test route"""
    return "Hello World"
