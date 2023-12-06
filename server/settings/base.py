from os.path import join
from typing import List

from djangocodemirror.settings import *

from server.settings import BASE_DIR, env

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

#################
#  Middlewares  #
#################

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

###############
#  Databases  #
###############

DATABASES = {"default": env.db()}

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

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
    "django.contrib.humanize",
    "django.contrib.postgres",
]

THIRD_PARTY_APPS = [
    "guardian",
    "bootstrap5",
    "crispy_forms",
    "crispy_bootstrap5",
    "djangocodemirror",
]

LOCAL_APPS = [
    "apps.users",
    "apps.contests",
    "apps.tasks",
    "apps.submissions",
]

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
        "DIRS": [BASE_DIR / "templates"],
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

STATIC_ROOT = BASE_DIR / "static"

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

####################
#  Authentication  #
####################

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
]

LOGIN_REDIRECT_URL = "home"

LOGOUT_REDIRECT_URL = "home"

LOGIN_URL = "login"
REGISTER_URL = "register"

# The model to use to represent an user.
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-user-model

AUTH_USER_MODEL = "users.User"

#####################
#  Django Guardian  #
#####################

ANONYMOUS_USER_NAME = None

##################
#  Crispy Forms  #
##################

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"
