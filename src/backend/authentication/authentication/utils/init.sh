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

openssl genrsa -out $KEY_DIR/private.pem 2048

sleep 1
openssl rsa -in $KEY_DIR/private.pem -pubout -out $KEY_DIR/public.pem

# Apply database migrations first time
echo "Applying database migrations..."
if ! python manage.py makemigrations authentication --noinput; then
  echo "Migrations failed"
  exit 1
fi

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
gunicorn --bind 0.0.0.0:80 --workers=3 config.wsgi:application --reload --timeout 120
