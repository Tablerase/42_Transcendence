#!/bin/bash

# Only work if the database is not already initialized

# Stop the script if an error occurs
set -e

# Read the read-only user password from the Docker secret
readonly_password=$(cat $POSTGRES_READONLY_PASSWORD_FILE)

# Create the read-only user and grant read permissions
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE USER $POSTGRES_READONLY_USER WITH PASSWORD '$readonly_password';
  GRANT CONNECT ON DATABASE $POSTGRES_DB TO $POSTGRES_READONLY_USER;
  \c $POSTGRES_DB
  GRANT USAGE ON SCHEMA public TO $POSTGRES_READONLY_USER;
  GRANT SELECT ON ALL TABLES IN SCHEMA public TO $POSTGRES_READONLY_USER;
  ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO $POSTGRES_READONLY_USER;
EOSQL

# Grant role to monitor the database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  GRANT pg_monitor TO $POSTGRES_READONLY_USER;
EOSQL