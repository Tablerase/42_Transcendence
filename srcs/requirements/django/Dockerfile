# Official Base Image for Python 3.12 (https://hub.docker.com/_/python)
FROM python:3.12-slim

# install system dependencies (netcat is used to check for database network access availability and django server socket readiness)
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
## Prevents Python from writing pyc files to disc (reduces I/O operations and speeds up execution)
ENV PYTHONDONTWRITEBYTECODE 1
## Set python to be unbuffered so that outputs are sent immediately to the terminal (helps with docker logging)
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
RUN rm -rf /usr/src/app
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install dependencies
RUN pip install --upgrade pip
COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Configure the entrypoint
COPY ./tools/django_setup.sh /tmp/django_setup.sh
RUN chmod +x /tmp/django_setup.sh

# Copy the current directory contents of the app (./app) into the container at /usr/src/app
COPY ./app .

RUN mkdir -p /app/media && chmod -R 755 /app/media

# Run the application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
## Use Daphne as the ASGI server to serve Django Channels allowing for WebSockets
CMD ["daphne", "backend.asgi:application", "-u", "/usr/src/app/daphne.sock"]
ENTRYPOINT ["/tmp/django_setup.sh"]