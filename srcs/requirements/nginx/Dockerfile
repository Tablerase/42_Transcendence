# Base Image
FROM debian:11-slim

# Install packages
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
  nginx \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Setup Configurations

# # Configure NGINX to log to stdout and stderr
# RUN sed -i 's|access_log /var/log/nginx/access.log;|access_log /dev/stdout;|' /etc/nginx/nginx.conf && \
#     sed -i 's|error_log /var/log/nginx/error.log;|error_log /dev/stderr;|' /etc/nginx/nginx.conf

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
# -g daemon off;
# run nginx in foreground mode to allow docker to manage the process and not exit immediately
