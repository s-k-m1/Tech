#!/bin/bash
set -e

echo "=== SK Tech Deployment ==="

ENV=${1:-production}
COMPOSE_FILE="infra/docker-compose${ENV: +-$ENV}.yml"

if [ ! -f "$COMPOSE_FILE" ]; then
    echo "Compose file not found: $COMPOSE_FILE"
    exit 1
fi

echo "Deploying to $ENV environment..."

# Pull latest code
git pull origin main

# Build and start services
docker compose -f "$COMPOSE_FILE" build
docker compose -f "$COMPOSE_FILE" up -d

# Run migrations
docker compose -f "$COMPOSE_FILE" exec backend python manage.py migrate --noinput

# Collect static files
docker compose -f "$COMPOSE_FILE" exec backend python manage.py collectstatic --noinput

# Reload nginx
docker compose -f "$COMPOSE_FILE" exec nginx nginx -s reload

echo "=== Deployment complete ==="
