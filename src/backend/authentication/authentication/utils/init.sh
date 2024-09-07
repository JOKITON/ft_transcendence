#!/bin/sh
set -e

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for PostgreSQL to start..."
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
  done
fi

KEY_DIR="/authentication/secrets"
mkdir -p "$KEY_DIR"

if [ ! -f /authentication/secrets/public.pem ]; then
  curl -o /authentication/secrets/public.pem http://keys/api/v1/keys/public
  if ! openssl rsa -pubin -in /authentication/secrets/public.pem -text -noout >/dev/null 2>&1; then
    echo "Error: Fetched public key is not valid."
    exit 1
  fi
fi

if [ ! -f /authentication/secrets/private.pem ]; then
  curl -o /authentication/secrets/private.pem http://keys/api/v1/keys/private
  if ! openssl rsa -in /authentication/secrets/private.pem -check >/dev/null 2>&1; then
    echo "Error: Fetched private key is not valid."
    exit 1
  fi
fi

# Apply database migrations first time
echo "Applying database migrations..."
if ! python manage.py makemigrations authentication --noinput; then
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
gunicorn --bind 0.0.0.0:80 --workers=3 config.wsgi:application --reload --timeout 120
