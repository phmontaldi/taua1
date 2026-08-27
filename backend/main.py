from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from config import settings

if not settings.DATABASE_URL or not settings.JWT_SECRET:
    raise RuntimeError(
        "DATABASE_URL e JWT_SECRET são obrigatórios e não podem estar vazios (configure o .env)."
    )

from auth import JWTAuthMiddleware  # noqa: E402
from rate_limit import limiter  # noqa: E402
from routers import auth as auth_router  # noqa: E402
from routers import bares, turnos  # noqa: E402

app = FastAPI(title="Bar da Piscina · Conferência Diária API", version="0.1.0")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(JWTAuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(bares.router)
app.include_router(turnos.router)


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}
