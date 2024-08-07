#!/bin/bash

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
unapplied_migrations=$(python manage.py showmigrations --plan | grep '\[ \]')

if [ -n "$unapplied_migrations" ]; then
    echo "Applying database migrations"
    python manage.py migrate
else
    echo "No migrations to apply"
fi

# Start server
echo "Starting server"
exec "$@"