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
RUN mkdir -p /etc/nginx/ssl
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
  -nodes \
  -out /etc/nginx/ssl/transcendence.crt \
  -keyout /etc/nginx/ssl/transcendence.key \
  -subj "/C=${SSL_COUNTRY}/ST=${SSL_STATE}/L=${SSL_LOCATION}/O=${SSL_ORGANIZATION}/OU=${SSL_ORGANIZATION_UNIT}/CN=${SSL_COMMON_NAME}"

# # Configure NGINX to log to stdout and stderr
# RUN sed -i 's|access_log /var/log/nginx/access.log;|access_log /dev/stdout;|' /etc/nginx/nginx.conf && \
#     sed -i 's|error_log /var/log/nginx/error.log;|error_log /dev/stderr;|' /etc/nginx/nginx.conf

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
# -g daemon off;
# run nginx in foreground mode to allow docker to manage the process and not exit immediately
