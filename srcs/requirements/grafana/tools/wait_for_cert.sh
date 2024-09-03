#!/bin/bash
# This script waits for the SSL certificate to be created by Nginx before starting Grafana

set -e

echo "Waiting for SSL certificate to be created by Nginx container..."

# Timeout settings
TIMEOUT=300  # Timeout in seconds (e.g., 300 seconds = 5 minutes)
INTERVAL=5   # Interval between checks in seconds
ELAPSED=0

while [ ! -f "$GF_SERVER_CERT_KEY" -a ! -f "$GF_SERVER_CERT_FILE" ]; do
  if [ $ELAPSED -ge $TIMEOUT ]; then
    echo "Timeout reached. SSL certificate not found."
    exit 1
  fi
  sleep $INTERVAL
  ELAPSED=$((ELAPSED + INTERVAL))
done

echo "SSL certificate found. Starting Grafana..."

# Execute the original entrypoint script
/run.sh