# import os
# from pathlib import Path
# from dotenv import load_dotenv
# import dj_database_url

# # ----------------------------------------
# # BASE DIRECTORY & ENVIRONMENT
# # ----------------------------------------
# BASE_DIR = Path(__file__).resolve().parent.parent
# load_dotenv()  # Load variables from .env file

# # ----------------------------------------
# # SECURITY SETTINGS
# # ----------------------------------------
# SECRET_KEY = os.getenv(
#     'DJANGO_SECRET_KEY',
#     'DJANGO_SECRET_KEY'
   
# )

# DEBUG = os.getenv('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS = [
#     'ecommerse-production.up.railway.app',
#     'localhost',
#     '127.0.0.1'
# ]
# CSRF_TRUSTED_ORIGINS = [
#     'https://ecommerse-production.up.railway.app'
# ]

# # ----------------------------------------
# # APPLICATIONS
# # ----------------------------------------
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',

#     # Your custom apps
#     'store',
#     'cart',
#     'payment',
#     'chatbot',

#     # Third-party apps
#     'whitenoise.runserver_nostatic',
#     'paypal.standard.ipn',
# ]

# # ----------------------------------------
# # MIDDLEWARE
# # ----------------------------------------
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',  # Must come right after SecurityMiddleware
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'ecom.urls'

# # ----------------------------------------
# # TEMPLATES
# # ----------------------------------------
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates'],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#                 'cart.context_processors.cart',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'ecom.wsgi.application'

# # ----------------------------------------
# # DATABASE CONFIGURATION
# # ----------------------------------------

# # Custom switch: use Postgres locally if POSTGRES_LOCALLY=True
# USE_LOCAL_POSTGRES = os.getenv('POSTGRES_LOCALLY', 'False') == 'False'
# DATABASE_URL = os.getenv('DATABASE_URL')

# if DATABASE_URL and not USE_LOCAL_POSTGRES:
#     # --- Production / Railway ---
#     DATABASES = {
#         'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
#     }

# elif USE_LOCAL_POSTGRES:
#     # --- Local PostgreSQL ---
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': os.getenv('DB_NAME', 'railway'),
#             'USER': os.getenv('DB_USER', 'postgres'),
#             'PASSWORD': os.getenv('DB_PASSWORD', 'DB_PASSWORD_TG'),
#             'HOST': os.getenv('DB_HOST', 'postgres-slda.railway.internal'),
#             'PORT': os.getenv('DB_PORT', '5432'),
#         }
#     }
# else:
#     # --- Local SQLite (default fallback) ---
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }

# # ----------------------------------------
# # PASSWORD VALIDATION
# # ----------------------------------------
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]

# # ----------------------------------------
# # INTERNATIONALIZATION
# # ----------------------------------------
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# # ----------------------------------------
# # STATIC & MEDIA FILES
# # ----------------------------------------
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / 'static']
# STATIC_ROOT = BASE_DIR / 'staticfiles'

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# # ----------------------------------------
# # DEFAULT FIELD TYPE
# # ----------------------------------------
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # ----------------------------------------
# # PAYPAL SETTINGS
# # ----------------------------------------
# PAYPAL_TEST = True
# PAYPAL_RECEIVER_EMAIL = 'business@markettest.com'
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
    "django-insecure-h6b3-4j%4mdy=)djegypej)y+z6f#y=)5ng8tq$+jhw2j9$n)-"
)

DEBUG = os.getenv("DEBUG", "False") == "True"
POSTGRES_LOCAL = os.getenv("POSTGRES_LOCAL", "False") == "True"

ALLOWED_HOSTS = [
    "ecommerse-production.up.railway.app",
    "localhost",
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [
    "https://ecommerse-production.up.railway.app",
]

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
if POSTGRES_LOCAL:
    print("🧩 Using LOCAL PostgreSQL Database")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "ecom"),
            "USER": os.getenv("DB_USER", "postgres"),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }
else:
    print("🚀 Using PRODUCTION Railway PostgreSQL Database")
    DATABASES = {
        "default": dj_database_url.config(
            default=os.getenv("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True
        )
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
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

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
