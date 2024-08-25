#!/bin/bash

# Workdir
cd /usr/src/app

# Wait for postgres to start
timeout=15
echo "Waiting for postgres..."
while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.5
    timeout=$((timeout - 1))
    if [ $timeout -eq 0 ]; then
        echo "PostgreSQL failed to start"
        exit 1
    fi
done
echo "PostgreSQL started"

# Check for unapplied migrations
echo "Checking for unapplied migrations..."
unapplied_migrations=$(python manage.py makemigrations --dry-run --check 2>&1)

if [ "$unapplied_migrations" != "No changes detected" ]; then
    echo "Applying database migrations"
    python manage.py makemigrations
    python manage.py migrate
else
    echo "No migrations to apply"
fi

# Collect static files
echo "Collecting static files"
python manage.py collectstatic --noinput --clear

# Start server
echo "Starting server"
exec "$@"