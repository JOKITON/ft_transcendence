#!/bin/sh
set -e

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for PostgreSQL to start..."
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
  done
fi

KEY_DIR="/livechat/secrets"
mkdir -p "$KEY_DIR"

curl -o $KEY_DIR/public.pem http://auth/api/v1/auth/public
if ! openssl rsa -pubin -in /livechat/secrets/public.pem -text -noout >/dev/null 2>&1; then
  echo "Error: Fetched public key is not valid."
  exit 1
fi

# Collect static files
echo "Collecting static files..."
if ! python3 manage.py collectstatic --no-input; then
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
if ! python manage.py makemigrations livechat --noinput; then
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

export DJANGO_SETTINGS_MODULE=config.settings
# Start the Django development server
echo "Starting Django development server..."
daphne -b 0.0.0.0 -p 80 config.asgi:application
