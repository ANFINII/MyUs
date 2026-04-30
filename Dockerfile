FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/code \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH=/opt/venv/bin:$PATH

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    ffmpeg \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY myus/pyproject.toml myus/uv.lock ./
RUN uv sync --frozen --no-install-project

COPY myus/ ./

EXPOSE 8000
