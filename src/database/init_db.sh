#!/bin/sh
set -e

# Create schemas if they don't exist
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<-EOSQL
  CREATE SCHEMA IF NOT EXISTS jwt;
  CREATE SCHEMA IF NOT EXISTS pong;
EOSQL
