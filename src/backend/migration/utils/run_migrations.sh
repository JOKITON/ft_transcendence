#!/bin/sh
set -e # Exit immediately if a command exits with a non-zero status

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for PostgreSQL to start..."
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
  done
fi

sh run_auth.sh

sh run_pong.sh

sh run_friendship.sh

# Add more apps as needed

while :; do sleep 2073600; done