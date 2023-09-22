from os.path import join
from typing import List

from server.settings import APPS_DIR, BASE_DIR, env

######################
#  General Settings  #
######################

SECRET_KEY = env("DJANGO_SECRET_KEY", default="django-secret-key")

DEBUG = env.bool("DJANGO_DEBUG", default=True)

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [join(BASE_DIR, "locale")]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#################
#  Middlewares  #
#################

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

###############
#  Databases  #
###############

DATABASES = {"default": env.db()}

##########
#  URLs  #
##########

ROOT_URLCONF = "server.urls"

WSGI_APPLICATION = "server.wsgi.application"

##########
#  Apps  #
##########

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS: List[str] = []

LOCAL_APPS: List[str] = []

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

###############
#  Passwords  #
###############

# The list of validators that are used to check the strength of user's
# passwords. See Password validation for more details.
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

BASE_PASSWORD_VALIDATOR = "django.contrib.auth.password_validation"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"{BASE_PASSWORD_VALIDATOR}.UserAttributeSimilarityValidator"},
    {"NAME": f"{BASE_PASSWORD_VALIDATOR}.MinimumLengthValidator"},
    {"NAME": f"{BASE_PASSWORD_VALIDATOR}.CommonPasswordValidator"},
    {"NAME": f"{BASE_PASSWORD_VALIDATOR}.NumericPasswordValidator"},
]

###############
#  Templates  #
###############

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [APPS_DIR / "templates"],
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

##################
#  Static files  #
##################

STATIC_URL = "/static/"
