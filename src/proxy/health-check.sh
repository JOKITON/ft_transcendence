#!/bin/bash

check_health() {
  local url=$1
  while true; do
    response=$(curl -s -o /dev/null -w "%{http_code}" $url)
    if [ "$response" -eq 200 ]; then
      echo "Health check passed for $url"
      break
    else
      echo "Waiting for $url to be healthy..."
      sleep 5
    fi
  done
}

# Check health for each service
check_health http://auth:80/api/v1/auth/health
check_health http://pong/api/v1/pong/health
check_health http://friendship/api/v1/friendship/health

echo "All services are healthy."

nginx -g "daemon off;"