FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root --only main

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY src ./src/

COPY entrypoint.sh ./
COPY migrations ./
COPY alembic.ini ./

EXPOSE 8000