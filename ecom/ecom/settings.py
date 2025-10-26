import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# -------------------------------
# BASE & ENV
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()  # Load .env file if present

# -------------------------------
# SECURITY
# -------------------------------
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-h6b3-4j%4mdy=)djegypej)y+z6f#y=)5ng8tq$+jhw2j9$n)-'
)

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['ecommerse-production.up.railway.app', 'https://ecommerse-production.up.railway.app']
CSRF_TRUSTED_ORIGINS = ['https://ecommerse-production.up.railway.app']


# -------------------------------
# APPS
# -------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps
    'store',
    'cart',
    'payment',
    'chatbot',
    'whitenoise.runserver_nostatic',
]

# -------------------------------
# MIDDLEWARE
# -------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'ecom.urls'

# -------------------------------
# TEMPLATES
# -------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecom.wsgi.application'

# -------------------------------
# DATABASES
# -------------------------------
# Default: SQLite (for local use)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Override with PostgreSQL if Railway or .env variables exist
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL, conn_max_age=600)
else:
    # Manual Railway connection fallback
    DB_HOST = os.getenv('DB_HOST', 'containers-us-west-42.railway.app')
    DB_NAME = os.getenv('DB_NAME', 'railway')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.environ['DB_PASSWORD_TG']
    DB_PORT = os.getenv('DB_PORT', '5432')

    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }

# -------------------------------
# PASSWORD VALIDATION
# -------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------
# INTERNATIONALIZATION
# -------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -------------------------------
# STATIC & MEDIA FILES
# -------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

#whitenoise noise static stuff
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -------------------------------
# DEFAULT FIELD TYPE
# -------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
