#import os
#import dj_database_url



#DATABASES = {'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))}


#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# MEDIA_ROOT = BASE_DIR / "media"

# # -------------------------------
# # DEFAULT FIELD TYPE
# # -------------------------------
# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# # -------------------------------
# # PAYPAL SETTINGS
# # -------------------------------
# PAYPAL_TEST = True
# PAYPAL_RECEIVER_EMAIL = "business@markettest.com"
import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# -------------------------------
# BASE & ENV
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()  # Load .env file

# -------------------------------
# SECURITY
# -------------------------------
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-default-key"
)

#DEBUG = os.getenv("DEBUG", "True") == "True"
DEBUG = os.getenv("DEBUG", "False") == "True"

#ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS","localhost 127.0.0.1 ecommerse-96t7.onrender.com").split()
ALLOWED_HOSTS = ['https://ecommerse-96t7.onrender.com']


CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS","https://ecommerse-96t7.onrender.com").split()

# -------------------------------
# APPS
# -------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Your apps
    "store",
    "cart",
    "payment",
    "chatbot",

    # Third-party apps
    "whitenoise.runserver_nostatic",
    "paypal.standard.ipn",
]

# -------------------------------
# MIDDLEWARE
# -------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -------------------------------
# URLS & WSGI
# -------------------------------
ROOT_URLCONF = "ecom.urls"
WSGI_APPLICATION = "ecom.wsgi.application"

# -------------------------------
# TEMPLATES
# -------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cart.context_processors.cart",
            ],
        },
    },
]

# -------------------------------
# DATABASES
# -------------------------------
DATABASES = {
    #"default": dj_database_url.config(default=os.getenv("DATABASE_URL"), conn_max_age=600, ssl_require=True)
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

# -------------------------------
# PASSWORD VALIDATION
# -------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------------------
# INTERNATIONALIZATION
# -------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -------------------------------
# STATIC & MEDIA FILES
# -------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
#STATIC_ROOT = BASE_DIR / "staticfiles"
#STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# -------------------------------
# DEFAULT FIELD TYPE
# -------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------------
# PAYPAL SETTINGS
# -------------------------------
PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL = "business@markettest.com"
