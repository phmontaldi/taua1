import secrets

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp

from config import settings

EXEMPT_PATHS = {"/api/v1/health", "/health"}


class ApiKeyMiddleware(BaseHTTPMiddleware):
    """Exige o header X-API-Key em todas as rotas, exceto /health."""

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS" or request.url.path in EXEMPT_PATHS:
            return await call_next(request)

        api_key = request.headers.get("X-API-Key", "")
        if not secrets.compare_digest(api_key, settings.API_KEY):
            return JSONResponse(
                status_code=401, content={"detail": "API key ausente ou inválida"}
            )

        return await call_next(request)
