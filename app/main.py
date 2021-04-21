"""
Run server
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """Test route"""
    return "Hello World"
