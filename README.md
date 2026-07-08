# Tauá · Conferência Diária do Bar

Aplicação de checklist e auditoria para a conferência diária dos bares Tauá. PWA em React (Vite) com fila de envios offline, consumindo uma API FastAPI com autenticação de líder (JWT) e persistência em PostgreSQL.

## Arquitetura

```
┌─────────────────────────┐        HTTPS/JSON        ┌──────────────────────────┐
│   Frontend (Vercel)     │ ────────────────────────▶ │   Backend (Railway/      │
│   Vite + React + PWA    │ ◀──────────────────────── │   Render) · FastAPI      │
│   fila offline (idb)    │        VITE_API_URL        │   + uvicorn + Alembic    │
└─────────────────────────┘                            └────────────┬─────────────┘
                                                                     │ asyncpg (SSL)
                                                                     ▼
                                                          ┌──────────────────────────┐
                                                          │   PostgreSQL (Neon)      │
                                                          └──────────────────────────┘
```

- **Frontend**: `src/` — SPA em React 18 + Vite 5, empacotada como PWA (`vite-plugin-pwa`) com fila de envios offline via IndexedDB (`idb`). Fala com o backend através de `VITE_API_URL` (`src/services/api.js`).
- **Backend**: `backend/` — API FastAPI (`backend/main.py`), SQLAlchemy 2.0 assíncrono (`asyncpg`), autenticação de líder via JWT (`backend/auth.py`), rate limiting (`slowapi`), migrações com Alembic (`backend/migrations/`). Gerenciado com [uv](https://docs.astral.sh/uv/).
- **Banco de dados**: PostgreSQL. Uma única variável `DATABASE_URL` é usada tanto pela aplicação (`backend/database.py`) quanto pelas migrações do Alembic (`backend/migrations/env.py`).

## Setup local

### Pré-requisitos

- Node.js 20+ e npm
- Python 3.11+ e [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Um PostgreSQL local (ou uma branch de dev no Neon)

### Backend

```bash
cd backend
cp .env.example .env        # ajuste DATABASE_URL e gere um JWT_SECRET
uv sync
uv run alembic upgrade head
uv run uvicorn main:app --reload --port 8000
```

Gere o `JWT_SECRET` com:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Frontend

```bash
cp .env.example .env         # VITE_API_URL=http://localhost:8000
npm install
npm run dev
```

A aplicação sobe em `http://localhost:5173` e consome a API em `http://localhost:8000`.

### Testes do backend

```bash
cd backend
uv sync --extra dev
uv run pytest
```

## Variáveis de ambiente

### Frontend (raiz do projeto, `.env`)

| Variável        | Descrição                                            | Exemplo                     |
|-----------------|-------------------------------------------------------|------------------------------|
| `VITE_API_URL`  | URL base da API backend, sem barra final              | `https://taua1-backend.up.railway.app` |

### Backend (`backend/.env`)

| Variável         | Descrição                                                                 | Exemplo                                                              |
|------------------|-----------------------------------------------------------------------------|-----------------------------------------------------------------------|
| `DATABASE_URL`   | Connection string do PostgreSQL, com driver `asyncpg`                       | `postgresql+asyncpg://user:pass@host:5432/db?ssl=require`             |
| `JWT_SECRET`     | Segredo usado para assinar/validar os tokens JWT de líder                   | gerado com `secrets.token_hex(32)`                                     |
| `CORS_ORIGINS`   | Lista de origens permitidas, separadas por vírgula (sem espaços/barra final)| `http://localhost:5173,https://taua1.vercel.app`                       |
| `ENVIRONMENT`    | Rótulo informativo do ambiente                                              | `production`                                                           |

`DATABASE_URL` e `JWT_SECRET` são obrigatórias — a API falha ao subir (`RuntimeError`) se qualquer uma estiver vazia (`backend/main.py`).

> **Neon + asyncpg**: use `?ssl=require` na connection string (não `?sslmode=require`, que é a sintaxe do `psycopg2` e não é reconhecida pelo driver `asyncpg`).

## Deploy

### 1. Banco de dados — Neon (PostgreSQL)

1. Crie uma conta em [neon.tech](https://neon.tech) e um novo projeto.
2. Crie um banco (ou use o `main` criado por padrão) e copie a **connection string** no formato "Pooled connection" (recomendado para uso com serviços serverless/instâncias que escalam).
3. Ajuste a connection string para o driver assíncrono usado pelo backend:
   - Neon fornece algo como `postgresql://user:pass@ep-xxxx.region.aws.neon.tech/dbname?sslmode=require`
   - Troque para: `postgresql+asyncpg://user:pass@ep-xxxx.region.aws.neon.tech/dbname?ssl=require`
4. Guarde essa URL — ela vai virar a variável `DATABASE_URL` do backend.

### 2. Backend — Railway ou Render

O repositório já inclui os arquivos de configuração:
- `backend/Procfile` e `backend/railway.json` (Railway)
- `render.yaml` na raiz (Render, Blueprint)

Ambos executam `alembic upgrade head` antes de subir o `uvicorn`, garantindo que as migrações rodem a cada deploy.

#### Opção A — Railway

1. Crie um projeto novo em [railway.app](https://railway.app) → **Deploy from GitHub repo** → selecione este repositório.
2. Em **Settings → Root Directory**, defina `backend` (o repositório é um monorepo).
3. Railway detecta o `railway.json` e usa Nixpacks com o `buildCommand`/`startCommand` já configurados (instala `uv`, roda `uv sync`, depois `alembic upgrade head` e `uvicorn`).
4. Em **Variables**, defina:
   - `DATABASE_URL` (connection string do Neon, com `+asyncpg` e `?ssl=require`)
   - `JWT_SECRET`
   - `CORS_ORIGINS` (inicialmente `http://localhost:5173`; volte aqui depois de publicar o frontend)
   - `ENVIRONMENT=production`
5. Railway expõe a porta via `$PORT` automaticamente — nada a fazer, o `startCommand` já usa essa variável.
6. Gere um domínio público em **Settings → Networking → Generate Domain**. Esse será o valor de `VITE_API_URL` no frontend.

#### Opção B — Render

1. Em [render.com](https://render.com), **New → Blueprint**, aponte para este repositório — o Render lê o `render.yaml` da raiz automaticamente.
2. Confirme o serviço `taua1-backend` (root dir `backend`, build/start commands já definidos).
3. Quando solicitado, preencha os secrets marcados como `sync: false`:
   - `DATABASE_URL`, `JWT_SECRET`, `CORS_ORIGINS`
4. O healthcheck já está configurado para `GET /api/v1/health`.
5. Após o primeiro deploy, copie a URL pública (`https://taua1-backend.onrender.com`) — será o `VITE_API_URL` do frontend.

> Se preferir não usar o Blueprint, configure manualmente um Web Service com Root Directory `backend`, Build Command `pip install uv && uv sync --frozen` e Start Command `uv run alembic upgrade head && uv run uvicorn main:app --host 0.0.0.0 --port $PORT`.

### 3. Frontend — Vercel

1. Em [vercel.com](https://vercel.com), **Add New → Project**, importe este repositório.
2. Vercel detecta o framework Vite automaticamente (também há um `vercel.json` na raiz com `buildCommand`/`outputDirectory` explícitos).
3. Em **Settings → Environment Variables**, adicione:
   - `VITE_API_URL` = URL pública do backend (Railway ou Render, sem barra final)
4. Deploy. O domínio de produção terá o formato `https://<nome-do-projeto>.vercel.app` (visível em **Settings → Domains**).

### 4. Fechar o CORS

Depois que o frontend estiver publicado na Vercel:

1. Copie o domínio de produção da Vercel (ex.: `https://taua1.vercel.app`).
2. No backend (Railway ou Render), atualize a variável `CORS_ORIGINS` para incluir esse domínio, mantendo o `localhost` do desenvolvimento se quiser continuar testando localmente contra o backend de produção:
   ```
   CORS_ORIGINS=http://localhost:5173,https://taua1.vercel.app
   ```
3. Redeploy o backend para aplicar a nova variável.

Se você adicionar um domínio customizado na Vercel, inclua-o também em `CORS_ORIGINS`. Deployments de preview da Vercel geram subdomínios únicos a cada push — para liberá-los no CORS, adicione a URL de preview específica caso precise testar contra o backend de produção a partir dela.

## Estrutura do repositório

```
.
├── src/                 # frontend (React + Vite + PWA)
├── backend/             # API FastAPI
│   ├── main.py          # entrypoint (app FastAPI, CORS, middlewares, routers)
│   ├── config.py         # leitura das variáveis de ambiente
│   ├── database.py       # engine assíncrono SQLAlchemy
│   ├── migrations/       # Alembic (script_location)
│   ├── routers/          # rotas de auth e turnos
│   └── services/         # regras de negócio (scoring, turnos)
├── render.yaml           # Blueprint de deploy do backend no Render
└── vercel.json           # configuração de build do frontend na Vercel
```
