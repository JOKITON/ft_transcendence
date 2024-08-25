#!/bin/sh
set -e

echo "Starting Django development server..."
gunicorn --bind 0.0.0.0:80 --workers=3 config.wsgi:application --reload --timeout 120
