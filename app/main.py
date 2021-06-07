"""
Run server
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .users.endpoints import router as user_router
from .content.endpoints import router as content_router
from .applications.endpoints import router as application_router
from .settings import get_origin_settings, DEBUG, IMG_PATH

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    **get_origin_settings()
)

app.include_router(user_router)
app.include_router(application_router)
app.include_router(content_router)

if DEBUG:
    if not os.path.isdir(IMG_PATH):
        os.mkdir(IMG_PATH)
    app.mount("/images", StaticFiles(directory=IMG_PATH), name="images")
