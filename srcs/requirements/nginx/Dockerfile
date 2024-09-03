# Base Image
FROM debian:11-slim

# Install packages
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
  nginx \
  openssl \
  curl \
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

# Set permissions for certificate files
RUN chmod 600 /etc/certs/key.pem
RUN chmod 644 /etc/certs/cert.pem

# # Configure NGINX to log to stdout and stderr
# RUN sed -i 's|access_log /var/log/nginx/access.log;|access_log /dev/stdout;|' /etc/nginx/nginx.conf && \
#     sed -i 's|error_log /var/log/nginx/error.log;|error_log /dev/stderr;|' /etc/nginx/nginx.conf

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
# -g daemon off;
# run nginx in foreground mode to allow docker to manage the process and not exit immediately
