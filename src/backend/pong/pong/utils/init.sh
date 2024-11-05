#!/bin/sh
set -e

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for PostgreSQL to start..."
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
  done
fi

sh utils/get_keys.sh

# Collect static files
echo "Collecting static files..."
if ! python manage.py collectstatic --no-input; then
  echo "Collectstatic failed"
  exit 1
fi

# Check if migration is running
while [ -f /migration/migration.lock ];
do
  echo "Waiting for migration to finish..."
  sleep 5
done

# Create migration.lock
if ! touch /migration/migration.lock; then
  echo "Failed to create migration.lock"
  exit 1
fi

# Apply database migrations
echo "Applying database migrations..."
if ! python manage.py makemigrations pong --noinput; then
  echo "Migrate failed"
  exit 1
fi

if ! python manage.py migrate --noinput; then
  echo "Migrate failed"
  exit 1
fi

# Remove migration.lock
if ! rm /migration/migration.lock; then
  echo "Failed to remove migration.lock"
  exit 1
fi

# Start the Django development server
echo "Starting Django development server..."
exec gunicorn --bind 0.0.0.0:80 --workers=3 config.wsgi:application --reload --timeout 120
