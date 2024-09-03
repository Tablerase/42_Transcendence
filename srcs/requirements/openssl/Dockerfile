# Base Image
FROM debian:12-slim

# Install packages
RUN apt-get update && apt-get install -y \
  openssl \
  && rm -rf /var/lib/apt/lists/*

# Setup Configurations
## ssl certificate
RUN mkdir -p /etc/certs
### Get arguments from docker-compose.yml
ARG SSL_COUNTRY
ARG SSL_STATE
ARG SSL_LOCATION
ARG SSL_ORGANIZATION
ARG SSL_ORGANIZATION_UNIT
ARG SSL_COMMON_NAME
### Generate SSL certificate
RUN openssl req \
  -x509 \
  -newkey rsa:4096 \
  -keyout /etc/certs/key.pem \
  -out /etc/certs/cert.pem \
  -days 365 \
  -nodes \
  -subj "/C=${SSL_COUNTRY}/ST=${SSL_STATE}/L=${SSL_LOCATION}/O=${SSL_ORGANIZATION}/OU=${SSL_ORGANIZATION_UNIT}/CN=${SSL_COMMON_NAME}"

# Add permissions for certificate files
## Grafana user (UID 472) is used in the Grafana image
RUN chown -R 472:472 /etc/certs