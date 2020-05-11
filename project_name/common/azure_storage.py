import mimetypes

import azure
from azure.storage.blob import BlockBlobService, ContentSettings
from django.conf import settings
from django.core.files.storage import Storage

try:
    from django.utils.deconstruct import deconstructible
except ImportError:
    # Support for django 1.7 and below
    def deconstructible(func):
        return func


@deconstructible
class AzureStorage(Storage):
    """
    Custom file storage system for Azure
    """

    container_name = settings.AZURE_CONTAINER
    account_name = settings.AZURE_ACCOUNT_NAME
    sas_token = settings.AZURE_SAS_TOKEN

    def __init__(self, *args, **kwargs):
        super(AzureStorage, self).__init__(*args, **kwargs)
        self._connection = None

    @property
    def connection(self):
        if not self._connection:
            self._connection = BlockBlobService(account_name=self.account_name,
                                                sas_token=self.sas_token)
        return self._connection

    def _open(self, name, mode=None):
        """
        Return the AzureStorageFile.
        """
        from django.core.files.base import ContentFile
        blob = self.connection.get_blob_to_bytes(self.container_name, name)
        content_file = ContentFile(blob.content)
        content_file.content_type = blob.properties.content_settings.content_type
        return content_file

    def size(self, name):
        blob = self.connection.get_blob_to_bytes(self.container_name, name)
        return blob.properties.content_length

    def _save(self, name, content):
        """
        Use the Azure Storage service to write ``content`` to a remote file
        (called ``name``).
        """
        if hasattr(content.file, 'content_type'):
            content_type = content.file.content_type
        else:
            content_type = mimetypes.guess_type(name)[0]

        self.connection.create_blob_from_stream(
            container_name=self.container_name,
            blob_name=name,
            stream=content,
            count=content.size,
            content_settings=ContentSettings(content_type=content_type))
        return name

    def exists(self, name):
        try:
            self.connection.get_blob_properties(self.container_name, name)
        except azure.common.AzureMissingResourceHttpError:
            return False
        else:
            return True

    def url(self, name):
        """
        Returns the URL where the contents of the file referenced by name can
        be accessed.
        return self.connection.make_blob_url(
            **blob_url_args
        )#+'?'+self.sas_token ---> Add token from url.

        """
        blob_url_args = {
            'container_name': self.container_name,
            'blob_name': name,
        }

        # BAD FIX!!!!!!!!!!
        if not name.startswith('/media/'):
            name = '/media/' + name

        # # Sending relative url
        # print(name)
        return self.connection.make_blob_url(**blob_url_args)

        # # Add this to send azure urls
        # return self.connection.make_blob_url(
        #     **blob_url_args
        # )+'?'+self.sas_token

    def delete(self, name):
        """
        Deletes the file referenced by name.
        """
        try:
            self.connection.delete_blob(self.container_name, name)
        except azure.common.AzureMissingResourceHttpError:
            pass
