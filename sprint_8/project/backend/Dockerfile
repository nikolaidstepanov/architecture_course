# Используем Python 3.9
FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY ./app ./app

ENV PORT=8000
ENV FASTAPI_APP_KEYCLOAK_URL=http://keycloak:8080
ENV FASTAPI_APP_KEYCLOAK_REALM=reports-realm
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]