# Etapa 1: Construir el Frontend (React/Vite)
FROM node:22-alpine AS frontend-builder
WORKDIR /app/web

# Habilitar pnpm
RUN corepack enable && corepack prepare pnpm@11.1.1 --activate

# Instalar dependencias web y compilar
COPY web/package.json web/pnpm-lock.yaml web/pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile
COPY web/ ./
RUN pnpm build

# Etapa 2: Construir el Backend (Python/FastAPI) y unir todo
FROM python:3.11-slim
WORKDIR /app

# Instalar gcc y build-essential (Obligatorio para que compile clipspy en la nube)
RUN apt-get update && apt-get install -y gcc build-essential

# Copiar archivos del proyecto Python
COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY clips/ ./clips/
COPY assets/ ./assets/

# Instalar la API y el motor de CLIPS
RUN pip install --no-cache-dir .

# Copiar el frontend compilado de la Etapa 1
COPY --from=frontend-builder /app/web/dist ./web/dist
COPY --from=frontend-builder /app/web/public ./web/public

ENV APP_ROOT=/app
ENV PORT=8000
EXPOSE 8000

# Render inyecta PORT; en local usa 8000 por defecto.
CMD ["sh", "-c", "uvicorn pricing_expert.api.main:app --host 0.0.0.0 --port ${PORT}"]