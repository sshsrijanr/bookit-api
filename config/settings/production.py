import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

ALLOWED_HOSTS = ['*']

DEBUG = False

try:
    from .local import *
except ImportError:
    pass

# Sentry Configuration
sentry_sdk.init(dsn=get_secret('SENTRY_DSN'),
                integrations=[DjangoIntegration()])
