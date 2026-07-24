FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings.prod

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY backend/requirements/prod.txt .
RUN pip install --no-cache-dir -r prod.txt

COPY backend/ .

CMD ["celery", "-A", "config.celery", "beat", "--loglevel=info"]
