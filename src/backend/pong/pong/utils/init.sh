#!/bin/sh

set -e

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for PostgreSQL to start..."
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
  done
fi

# Generate RSA keys if they don't exist
KEY_DIR="/pong/secrets"
mkdir -p "$KEY_DIR"

# Fetch public key from JWT Key Management Service
curl -o /pong/secrets/public.pem http://keys/api/v1/keys/public
if ! openssl rsa -pubin -in /pong/secrets/public.pem -text -noout >/dev/null 2>&1; then
  echo "Error: Fetched public key is not valid."
  exit 1
fi

# Apply database migrations first time
echo "Applying database migrations..."
if ! python manage.py makemigrations --noinput; then
  echo "Migrations failed"
  exit 1
fi

# Apply database migrations
echo "Applying database migrations..."
if ! python manage.py migrate --noinput; then
  echo "Migrations failed"
  exit 1
fi

# Collect static files
echo "Collecting static files..."
if ! python manage.py collectstatic --no-input; then
  echo "Collectstatic failed"
  exit 1
fi

# Start the Django development server
echo "Starting Django development server..."
exec gunicorn --bind 0.0.0.0:80 --workers=3 config.wsgi:application --reload --timeout 120
