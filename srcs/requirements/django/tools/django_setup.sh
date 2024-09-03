#!/bin/bash

# Workdir
cd /usr/src/app

# Wait for postgres to start
timeout=180
interval=1
echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep $(interval)
    timeout=$((timeout - $(interval)))
    if [ $timeout -eq 0 ]; then
        echo "PostgreSQL failed to start"
        exit 1
    fi
done
echo "PostgreSQL started"

# Check for unapplied migrations
echo "Checking for unapplied migrations..."
python manage.py makemigrations --noinput
python manage.py migrate

# Collect static files
echo "Collecting static files"
python manage.py collectstatic --noinput --clear

rm -rf /usr/src/app/daphne.sock
rm -rf /usr/src/app/daphne.sock.lock
# Start server
echo "Starting server"
exec "$@"