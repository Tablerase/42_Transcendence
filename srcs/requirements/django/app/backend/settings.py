"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open(os.getenv('DJANGO_SECRET_KEY_FILE', '/run/secrets/django_secret_key'), 'r') as f:
    password_django = f.read().strip() # Remove the trailing newline or whitespace
SECRET_KEY = password_django

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Protection against Arbitrary Host Header Injection
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost').split(' ')
CSRF_TRUSTED_ORIGINS = [
    scheme + host for host in ALLOWED_HOSTS for scheme in ['https://', 'http://']
]

# Application definition
INSTALLED_APPS = [
    'crispy_forms',
    'crispy_bootstrap5',
    'daphne',
    "chat.apps.ChatConfig",
    "users.apps.UsersConfig",
    "game.apps.GameConfig",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# Application definition
ASGI_APPLICATION = 'backend.asgi.application'
WSGI_APPLICATION = 'backend.wsgi.application'

# Channels
# https://channels.readthedocs.io/en/stable/index.html
## For more persistent connections, we can use a Redis channel layer
CHANNEL_LAYERS = { 
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }   
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
## Retrieve the PostgreSQL password from a secret file
with open(os.getenv('POSTGRES_USER_PASSWORD_FILE', '/run/secrets/db_password'), 'r') as f:
    postgresql_password = f.read().strip() # Remove the trailing newline or whitespace

DATABASES = {
    # PostgreSQL database
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': postgresql_password,
        'HOST': os.environ.get('SQL_HOST'), # Service name in docker-compose
        'PORT': os.environ.get('SQL_PORT'), # postgres port
    }
    # sqlite3 database
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = 'bootstrap5'

LOGIN_REDIRECT_URL = 'chat-home'
LOGIN_URL = 'login'

AUTH_USER_MODEL = 'users.CustomUser'
