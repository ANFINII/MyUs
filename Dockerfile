FROM python:3.15-slim

ARG UV_SYNC_ARGS="--no-dev"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/code \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH=/opt/venv/bin:$PATH

COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /usr/local/bin/

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    ffmpeg \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY myus/pyproject.toml myus/uv.lock ./
RUN uv sync --frozen --no-install-project $UV_SYNC_ARGS

COPY myus/ ./

RUN useradd --create-home --uid 1000 app
USER app

EXPOSE 8000
