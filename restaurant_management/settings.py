"""
Django settings for restaurant_management project.
"""

from pathlib import Path
import os

# BASE DIR
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY
SECRET_KEY = 'django-insecure-s^x_u!itekxd=@a3o3zv4d%hw$j6d#2v358wgltxl8rc(-^t&p'
DEBUG = True
ALLOWED_HOSTS = ['*']   # Update for production


# APPLICATIONS
INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',

    # Project apps
    'home',
    'account',
    'home.products',   # ✔ Products app correctly under home/
    'orders',
]


# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'restaurant_management.urls'


# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Optional but recommended: global templates folder
        'DIRS': [BASE_DIR / 'templates'],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'restaurant_management.wsgi.application'


# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# STATIC FILES
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',     # for development assets
]
STATIC_ROOT = BASE_DIR / 'staticfiles'   # for collectstatic (production)


# MEDIA FILES
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755


# DEFAULT PK TYPE
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# -----------------------------
# CUSTOM RESTAURANT SETTINGS
# -----------------------------

RESTAURANT_NAME = "Gourmet Delight"
RESTAURANT_TAGLINE = "Exquisite Dining Experience"

RESTAURANT_ADDRESS = "123 Gourmet Street, Foodville, FC 12345"
RESTAURANT_PHONE = "+1 (555) 123-4567"
RESTAURANT_EMAIL = "info@restaurant.com"

RESTAURANT_HOURS = {
    'weekdays': 'Mon - Fri: 11:00 AM - 9:00 PM',
    'weekend': 'Sat - Sun: 10:00 AM - 10:00 PM',
    'special': 'Holiday hours may vary'
}

RESTAURANT_GOOGLE_MAPS_EMBED_URL = (
    "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!"
    "1d3022.9663095343004!2d-74.004258724269!3d40.74076987138915!"
    "2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!"
    "3m3!1m2!1s0x89c259bf5c8eef01%3A0x830f84cef0b8c03e!"
    "2s123%20Gourmet%20St%2C%20New%20York%2C%20NY%2010001%2C%20USA!"
    "5e0!3m2!1sen!2s!4v1693424567890!5m2!1sen!2s"
)
