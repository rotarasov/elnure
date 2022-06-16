from collections import OrderedDict
from datetime import timedelta
from pathlib import Path

import environ
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add .env file to environmental variables
env = environ.Env(DJANGO_DEBUG=(bool, True))

environ.Env.read_env()


SECRET_KEY = env.str("DJANGO_SECRET_KEY")

DEBUG = env.bool("DJANGO_DEBUG")

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "constance",
    "constance.backends.database",
    "jazzmin",
    "elnure_api.apps.ElnureAdminConfig",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "rest_framework_simplejwt",
    "django_json_widget",
    "corsheaders",
    "elnure_common",
    "elnure_users",
    "elnure_core",
    "elnure_config",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "elnure_api.urls"

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

WSGI_APPLICATION = "elnure_api.wsgi.application"


DATABASES = {"default": env.db("DJANGO_DATABASE_URL")}

CACHES = {}
if env.bool("DJANGO_ENABLE_CACHE", False):
    CACHES["default"] = {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "127.0.0.1:11211",
    }

else:
    CACHES["default"] = {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "elnure_users.authentication.JWTCookieAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

SIMPLE_JWT = {
    "AUTH_COOKIE": "_access_tok",
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_COOKIE_SECURE": True,
    "AUTH_COOKIE_HTTP_ONLY": not DEBUG,
    "AUTH_COOKIE_SAMESITE": "Lax",
    "CONFIRM_AUTH_COOKIE": "_include_auth",
}


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = False

USE_TZ = True


STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model

AUTH_USER_MODEL = "elnure_users.User"


BASE_BACKEND_URL = env.str("DJANGO_BASE_BACKEND_URL")
BASE_FRONTEND_URL = env.str("DJANGO_BASE_FRONTEND_URL")


GOOGLE_OAUTH2_CLIENT_ID = env.str("DJANGO_GOOGLE_OAUTH2_CLIENT_ID")
GOOGLE_OAUTH2_CLIENT_SECRET = env.str("DJANGO_GOOGLE_OAUTH2_CLIENT_SECRET")
GOOGLE_OAUTH2_SCOPE = " ".join(
    [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ]
)


# Django Constance

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

CONSTANCE_DATABASE_CACHE_BACKEND = "default"

CONSTANCE_ADDITIONAL_FIELDS = {
    "strategy_select": [
        "django.forms.fields.ChoiceField",
        {"widget": "django.forms.Select", "choices": (("DEFAULT", "Default"),)},
    ],
    "semesters_field": ["elnure_common.admin.forms.fields.SemestersJSONField", {}],
}


CONSTANCE_CONFIG = OrderedDict(
    [
        (
            "SEMESTERS",
            (
                [3, 4, 5, 6, 7, 8],
                _("Semesters which should be formed elective groups for."),
                "semesters_field",
            ),
        ),
        (
            "STRATEGY",
            (
                "DEFAULT",
                _("Strategy to distribute students by elective courses."),
                "strategy_select",
            ),
        ),
        (
            "MAX_NUMBER_OF_STUDENTS_IN_ELECTIVE_GROUP",
            (
                20,
                _(
                    "Maximum number of students to be in elective group during student distribution."
                ),
            ),
        ),
        (
            "MIN_NUMBER_OF_STUDENTS_IN_ELECTIVE_GROUP",
            (
                5,
                _(
                    "Maximum number of students to be in elective group during student distribution. "
                    "Also it is taken as a minimum number of students on the elective course."
                ),
            ),
        ),
        (
            "MAX_NUMBER_OF_ELECTIVE_GROUPS",
            (
                5,
                _("Maximum number of electve groups for elective course."),
            ),
        ),
    ]
)


# Django-jazzmin admin panel

JAZZMIN_SETTINGS = {
    "site_logo": "admin/img/nure_se_logo.png",
    "welcome_sign": _("Welcome back!"),
    "custom_links": {
        "elnure_users": [
            {
                "name": _("Import user mappings"),
                "url": reverse_lazy("admin:import-user-mappings"),
            }
        ]
    },
}


# Django CORS

CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]

CORS_ALLOW_CREDENTIALS = True
