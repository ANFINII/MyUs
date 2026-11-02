FROM python:3.15-slim AS builder

ARG UV_SYNC_ARGS="--no-dev"

ENV UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv

COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /usr/local/bin/

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY myus/pyproject.toml myus/uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-install-project $UV_SYNC_ARGS


FROM python:3.15-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/code \
    PATH=/opt/venv/bin:$PATH

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    libmariadb3 \
    ffmpeg \
  && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv

WORKDIR /code

COPY myus/ ./

RUN useradd --create-home --uid 1000 app
USER app

EXPOSE 8000
