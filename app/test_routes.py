from re import match
from app.main import app


def test_routes():
    """
    Ensure routes have trailing slash
    """
    default_routes = ("/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc")
    assert all([match("/.+/", route.path) for route in app.routes if route.path not in default_routes])
