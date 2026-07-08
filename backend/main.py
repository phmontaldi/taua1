from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings

if not settings.DATABASE_URL or not settings.API_KEY:
    raise RuntimeError(
        "DATABASE_URL e API_KEY são obrigatórios e não podem estar vazios (configure o .env)."
    )

from auth import ApiKeyMiddleware  # noqa: E402
from routers import turnos  # noqa: E402

app = FastAPI(title="Bar da Piscina · Conferência Diária API", version="0.1.0")

app.add_middleware(ApiKeyMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(turnos.router)


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}
