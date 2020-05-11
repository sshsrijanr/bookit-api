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

FILE_STORAGE_LOCATION = 'AZURE'  # AZURE, LOCAL, AWS
if FILE_STORAGE_LOCATION == 'AZURE':
    DEFAULT_FILE_STORAGE = "common.azure_storage.AzureStorage"
    AZURE_ACCOUNT_NAME = get_secret('AZURE_ACCOUNT_NAME')
    AZURE_SAS_TOKEN = get_secret('AZURE_SAS_TOKEN')
    AZURE_CONTAINER = get_secret('AZURE_CONTAINER')
