from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

try:
    from .local import *
except ImportError:
    pass

DJANGO_APPS = ['django_extensions']

INSTALLED_APPS += DJANGO_APPS

FILE_STORAGE_LOCATION = 'AZURE'  # AZURE, LOCAL, AWS
if FILE_STORAGE_LOCATION == 'AZURE':
    DEFAULT_FILE_STORAGE = "common.azure_storage.AzureStorage"
    AZURE_ACCOUNT_NAME = get_secret('AZURE_ACCOUNT_NAME')
    AZURE_SAS_TOKEN = get_secret('AZURE_SAS_TOKEN')
    AZURE_CONTAINER = get_secret('AZURE_CONTAINER')
