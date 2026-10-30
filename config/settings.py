import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Lee el archivo .env en local. En producción, las variables las
# definirá la plataforma de despliegue, sin archivo .env.
load_dotenv(BASE_DIR / ".env")


def env_bool(nombre, defecto=False):
    """Lee una variable de entorno y la convierte en True/False."""
    return os.environ.get(nombre, str(defecto)).strip().lower() in ("1", "true", "yes", "si")


# Seguro por defecto: si no se indica nada, DEBUG está apagado
DEBUG = env_bool("DEBUG", False)

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ImproperlyConfigured("Falta la variable de entorno SECRET_KEY")

ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h.strip()]

CSRF_TRUSTED_ORIGINS = []
if DEBUG:
    # Solo en desarrollo: el servidor de Vite (puerto 5173)
    CSRF_TRUSTED_ORIGINS += ["http://localhost:5173", "http://127.0.0.1:5173"]

# Render (o la plataforma elegida) define esta variable con el dominio público
host_despliegue = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if host_despliegue:
    ALLOWED_HOSTS.append(host_despliegue)
    CSRF_TRUSTED_ORIGINS.append(f"https://{host_despliegue}")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'maintenance',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

# SQLite en desarrollo (sin DATABASE_URL); PostgreSQL cuando exista esa variable
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}


# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = 'static/'


# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

# --- Seguridad en producción (solo cuando DEBUG está apagado) ---
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600

# Ficheros subidos por los usuarios (documentos técnicos)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
