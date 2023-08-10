{% if cookiecutter.use_sentry == 'y' -%}
import logging

import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
# from sentry_sdk.integrations.redis import RedisIntegration

{% endif -%}
from .base import *  # noqa
from .base import config

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = config("DJANGO_SECRET_KEY")
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = config(
    "DJANGO_ALLOWED_HOSTS",
    cast=lambda v: [s.strip() for s in v.split(",")],
    default=["{{ cookiecutter.domain_name }}"],
)


# DATABASES
# ------------------------------------------------------------------------------
DATABASES["default"]["CONN_MAX_AGE"] = config("CONN_MAX_AGE", default=60)  # noqa: F405


# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = config("DJANGO_SECURE_SSL_REDIRECT", cast=bool, default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = config("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", cast=bool, default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = config("DJANGO_SECURE_HSTS_PRELOAD", cast=bool, default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = config("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", cast=bool, default=True)

{% if cookiecutter.cloud_provider != 'None' -%}
# STORAGES
# ------------------------------------------------------------------------------
# https://django-storages.readthedocs.io/en/latest/#installation
INSTALLED_APPS += ["storages"]  # noqa: F405
{%- endif -%}
{% if cookiecutter.cloud_provider == 'AWS' %}
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_ACCESS_KEY_ID = config("DJANGO_AWS_ACCESS_KEY_ID")
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_SECRET_ACCESS_KEY = config("DJANGO_AWS_SECRET_ACCESS_KEY")
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_STORAGE_BUCKET_NAME = config("DJANGO_AWS_STORAGE_BUCKET_NAME")
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_QUERYSTRING_AUTH = False
# DO NOT change these unless you know what you're doing.
_AWS_EXPIRY = 60 * 60 * 24 * 7
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate",
}
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_MAX_MEMORY_SIZE = config(
    "DJANGO_AWS_S3_MAX_MEMORY_SIZE",
    cast=int,
    default=100_000_000,  # 100MB
)
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_REGION_NAME = config("DJANGO_AWS_S3_REGION_NAME", default=None)
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#cloudfront
AWS_S3_CUSTOM_DOMAIN = config("DJANGO_AWS_S3_CUSTOM_DOMAIN", default=None)
aws_s3_domain = AWS_S3_CUSTOM_DOMAIN or f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
{% elif cookiecutter.cloud_provider == 'GCP' %}
GS_BUCKET_NAME = config("DJANGO_GCP_STORAGE_BUCKET_NAME")
GS_DEFAULT_ACL = "publicRead"
{% endif -%}

{% if cookiecutter.cloud_provider != 'None' or cookiecutter.use_whitenoise == 'y' %}
# STATIC
# ------------------------
{% endif -%}
{% if cookiecutter.use_whitenoise == 'y' -%}
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
{% elif cookiecutter.cloud_provider == 'AWS' -%}
STATICFILES_STORAGE = "{{cookiecutter.project_slug}}.utils.storages.StaticRootS3Boto3Storage"
COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"
STATIC_URL = f"https://{aws_s3_domain}/static/"
{% elif cookiecutter.cloud_provider == 'GCP' -%}
STATICFILES_STORAGE = "{{cookiecutter.project_slug}}.utils.storages.StaticRootGoogleCloudStorage"
COLLECTFAST_STRATEGY = "collectfast.strategies.gcloud.GoogleCloudStrategy"
STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"
{% endif -%}

{% if cookiecutter.cloud_provider != 'None' %}
# MEDIA
# ------------------------------------------------------------------------------
{%- endif %}
{%- if cookiecutter.cloud_provider == 'AWS' %}
DEFAULT_FILE_STORAGE = "{{cookiecutter.project_slug}}.utils.storages.MediaRootS3Boto3Storage"
MEDIA_URL = f"https://{aws_s3_domain}/media/"
{%- elif cookiecutter.cloud_provider == 'GCP' %}
DEFAULT_FILE_STORAGE = "{{cookiecutter.project_slug}}.utils.storages.MediaRootGoogleCloudStorage"
MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
{%- endif %}

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = config("DJANGO_ADMIN_URL")
{% if cookiecutter.use_whitenoise == 'n' %}
# Collectfast
# ------------------------------------------------------------------------------
# https://github.com/antonagestam/collectfast#installation
INSTALLED_APPS = ["collectfast"] + INSTALLED_APPS  # noqa: F405
{% endif %}
# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
{% if cookiecutter.use_sentry == 'n' -%}
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console", "mail_admins"],
            "propagate": True,
        },
    },
}
{% else %}
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        # Errors logged by the SDK itself
        "sentry_sdk": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# Sentry
# ------------------------------------------------------------------------------
SENTRY_DSN = config("SENTRY_DSN")
SENTRY_LOG_LEVEL = config("DJANGO_SENTRY_LOG_LEVEL", default=logging.INFO, cast=int)

sentry_logging = LoggingIntegration(
    level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)

integrations = [sentry_logging, DjangoIntegration()]
# integrations = [sentry_logging, DjangoIntegration(), RedisIntegration()]

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=integrations,
    environment=config("SENTRY_ENVIRONMENT", default="production"),
    traces_sample_rate=config("SENTRY_TRACES_SAMPLE_RATE", default=0.0, cast=float),
)
{% endif %}
{% if cookiecutter.rest_framework == 'DRF' -%}

# django-rest-framework
# -------------------------------------------------------------------------------
# Tools that generate code samples can use SERVERS to point to the correct domain
SPECTACULAR_SETTINGS["SERVERS"] = [  # noqa: F405
    {"url": "https://{{ cookiecutter.domain_name }}", "description": "Production server"},
]
{%- endif %}
# Your stuff...
# ------------------------------------------------------------------------------
