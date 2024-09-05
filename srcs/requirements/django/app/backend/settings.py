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
debug_mode = os.getenv('DJANGO_DEBUG', 'False')
DEBUG = debug_mode

# Protection against Arbitrary Host Header Injection
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost').split(' ')
CSRF_TRUSTED_ORIGINS = [
    scheme + host for host in ALLOWED_HOSTS for scheme in ['https://', 'http://']
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

# Application definition
INSTALLED_APPS = [
    'crispy_forms',
    'crispy_bootstrap5',
    'channels',
    'daphne',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'users.apps.UsersConfig',
    'game.apps.GameConfig',

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    
    'allauth.account.middleware.AccountMiddleware',
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
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}
# CHANNEL_LAYERS = { 
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer"
#     }   
# }

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
        'HOST': os.environ.get('POSTGRES_HOST'), # Service name in docker-compose
        'PORT': os.environ.get('POSTGRES_PORT'), # postgres port
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

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = 'bootstrap5'

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

AUTH_USER_MODEL = 'users.CustomUser'

AUTHENTICATION_BACKENDS = [
    'users.backends.UserBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Allauth settings

## Retrieve google api secret from a secret file
with open(os.getenv('GOOGLE_API_SECRET_FILE'), 'r') as f:
    google_api_secret = f.read().strip()

SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv("GOOGLE_API_ID"),
            'secret': google_api_secret,
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
    }
}

SOCIALACCOUNT_ADAPTER = 'users.adapters.MySocialAccountAdapter'

# Authentication through 42s API

## Retrieve the api 42 password from a secret file
with open(os.getenv('API_42_SECRET_FILE'), 'r') as f:
    api_42_secret = f.read().strip()
OAUTH42_CLIENT_ID = os.getenv("API_42_ID")
OAUTH42_CLIENT_SECRET = api_42_secret
OAUTH42_REDIRECT_URI = os.getenv("REDIRECT_URI")

from users.auth.oauth42 import Oauth42

CLIENT = Oauth42(OAUTH42_CLIENT_ID, OAUTH42_CLIENT_SECRET, OAUTH42_REDIRECT_URI)
