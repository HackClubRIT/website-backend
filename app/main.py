"""
Run server
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .users.endpoints import router as user_router
from .content.endpoints import router as content_router
from .applications.endpoints import router as application_router
from .settings import get_origin_settings, DEBUG

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    **get_origin_settings()
)

app.include_router(user_router)
app.include_router(application_router)
app.include_router(content_router)

if DEBUG:
    app.mount("/images", StaticFiles(directory="app/images"), name="images")
