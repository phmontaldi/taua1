FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Camada de cache: instala as dependências antes de copiar o código,
# assim mudanças no código não invalidam o cache de deps.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .
RUN uv sync --frozen --no-dev

CMD alembic upgrade head && uv run uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
