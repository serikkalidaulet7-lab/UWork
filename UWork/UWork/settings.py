import importlib.util
import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

DJANGO_ENV = os.environ.get("DJANGO_ENV", "development").lower()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if DJANGO_ENV == "production":
        raise ImproperlyConfigured("DJANGO_SECRET_KEY must be set in production.")
    SECRET_KEY = "dev-only-secret-key-not-for-production"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get(
    "DJANGO_DEBUG",
    "True" if DJANGO_ENV != "production" else "False",
).lower() in {"1", "true", "yes", "on"}

raw_allowed_hosts = os.environ.get('DJANGO_ALLOWED_HOSTS', '').strip()

if raw_allowed_hosts:
    allowed_hosts = {
        host.strip()
        for host in raw_allowed_hosts.split(',')
        if host.strip()
    }
else:
    allowed_hosts = {"localhost", "127.0.0.1"}

railway_public_domain = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '').strip()
running_on_railway = any(
    os.environ.get(var)
    for var in ('RAILWAY_PROJECT_ID', 'RAILWAY_SERVICE_ID', 'RAILWAY_ENVIRONMENT_ID', 'RAILWAY_PUBLIC_DOMAIN')
)

if railway_public_domain:
    allowed_hosts.add(railway_public_domain)
elif running_on_railway:
    # Allow Railway-generated public subdomains during first deploys.
    allowed_hosts.add('.up.railway.app')
    allowed_hosts.add("healthcheck.railway.app")
    allowed_hosts.add('.railway.internal')

# Railway deployment healthchecks use this hostname.
allowed_hosts.add('healthcheck.railway.app')

if DEBUG:
    allowed_hosts.add("0.0.0.0")

ALLOWED_HOSTS = ["*"] if "*" in allowed_hosts else sorted(allowed_hosts)

raw_csrf_trusted_origins = os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS', '').strip()
csrf_trusted_origins = {
    origin.strip()
    for origin in raw_csrf_trusted_origins.split(',')
    if origin.strip()
}

if railway_public_domain:
    csrf_trusted_origins.add(f'https://{railway_public_domain}')
elif running_on_railway:
    csrf_trusted_origins.add('https://*.up.railway.app')

for host in allowed_hosts:
    if host in {'*', 'healthcheck.railway.app'} or host.startswith('.'):
        continue
    if '://' in host:
        csrf_trusted_origins.add(host)
    else:
        csrf_trusted_origins.add(f'https://{host}')

CSRF_TRUSTED_ORIGINS = sorted(csrf_trusted_origins)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = DJANGO_ENV == "production"
CSRF_COOKIE_SECURE = DJANGO_ENV == "production"
SECURE_HSTS_SECONDS = 31536000 if DJANGO_ENV == "production" else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = DJANGO_ENV == "production"
SECURE_HSTS_PRELOAD = DJANGO_ENV == "production"


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',
]

whitenoise_installed = importlib.util.find_spec("whitenoise") is not None

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if whitenoise_installed:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

ROOT_URLCONF = 'UWork.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'UWork.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ.get('SQLITE_PATH', str(BASE_DIR / 'db.sqlite3')),
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
    if whitenoise_installed
    else 'django.contrib.staticfiles.storage.StaticFilesStorage'
)
