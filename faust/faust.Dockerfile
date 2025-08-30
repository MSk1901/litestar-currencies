FROM python:3.9-slim AS builder

WORKDIR /app

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && pip install poetry

COPY faust/pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root --only main

FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY faust/src ./src/

EXPOSE 8000