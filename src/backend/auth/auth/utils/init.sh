#!/bin/sh
set -e

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for PostgreSQL to start..."
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
  done
fi

KEY_DIR="/auth/secrets"
mkdir -p "$KEY_DIR"

curl -o /auth/secrets/public.pem http://keys/api/v1/keys/public
if ! openssl rsa -pubin -in /auth/secrets/public.pem -text -noout >/dev/null 2>&1; then
  echo "Error: Fetched public key is not valid."
  exit 1
fi

curl -o /auth/secrets/private.pem http://keys/api/v1/keys/private
if ! openssl rsa -in /auth/secrets/private.pem -check >/dev/null 2>&1; then
  echo "Error: Fetched private key is not valid."
  exit 1
fi

sleep 2

# Apply database migrations first time
echo "Applying database migrations..."
if ! python manage.py showmigrations; then
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
