from dataclasses import dataclass

import jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp

from config import settings

EXEMPT_PATHS = {"/api/v1/health", "/health", "/api/v1/auth/login"}
JWT_ALGORITHM = "HS256"


class JWTAuthMiddleware(BaseHTTPMiddleware):
    """Exige Authorization: Bearer <jwt> em todas as rotas, exceto login e health."""

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS" or request.url.path in EXEMPT_PATHS:
            return await call_next(request)

        scheme, _, token = request.headers.get("Authorization", "").partition(" ")
        if scheme.lower() != "bearer" or not token:
            return JSONResponse(
                status_code=401, content={"detail": "Token ausente ou inválido"}
            )

        try:
            claims = jwt.decode(token, settings.JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"detail": "Token expirado"})
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"detail": "Token inválido"})

        request.state.lider_id = claims.get("sub")
        request.state.lider_nome = claims.get("nome")

        return await call_next(request)


@dataclass(frozen=True)
class LiderAtual:
    id: str
    nome: str


def get_current_lider(request: Request) -> LiderAtual:
    return LiderAtual(id=request.state.lider_id, nome=request.state.lider_nome)
