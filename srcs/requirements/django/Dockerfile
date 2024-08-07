# Official Base Image for Python 3.12 (https://hub.docker.com/_/python)
FROM python:3.12-slim

# install system dependencies
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
## Prevents Python from writing pyc files to disc (reduces I/O operations and speeds up execution)
ENV PYTHONDONTWRITEBYTECODE 1
## Set python to be unbuffered so that outputs are sent immediately to the terminal (helps with docker logging)
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
RUN mkdir /app
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip
COPY ./app/requirements.txt .
RUN pip install -r requirements.txt

# Configure the entrypoint
COPY ./tools/django_setup.sh django_setup.sh
RUN chmod +x django_setup.sh

# Copy the current directory contents into the container at /app
COPY ./app/ .

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["/app/django_setup.sh"]