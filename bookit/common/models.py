import hashlib
import os
import time
import uuid
from mimetypes import MimeTypes

from django.db import models
from slugify import slugify


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EnumerationModel(models.Model):
    title = models.TextField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.title)


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          db_index=True)

    class Meta:
        abstract = True


class EnumeratedUUIDModel(EnumerationModel, UUIDModel):
    pass

    class Meta:
        abstract = True


class TimeStampedUUIDModel(UUIDModel, TimeStampedModel):
    pass

    class Meta:
        abstract = True


class TimeStampedEnumeratedUUIDModel(EnumeratedUUIDModel, TimeStampedModel):
    pass

    class Meta:
        abstract = True


def content_file_name(instance, filename):
    folder_name = {
        'images': ['jpeg', 'jpg', 'png'],
        'documents': ['pdf', 'doc', 'docx']
    }

    attachment_type = None
    if not instance.attachment_type:
        attachment_type = 'other'
        filepath = attachment_type + os.path.sep
    else:
        filepath = instance.attachment_type + os.path.sep

    # File Type
    file, ext = os.path.splitext(filename)
    ext = ext.replace('.', '').lower()
    for key in folder_name:
        if ext in folder_name[key]:
            filepath += key + os.path.sep

    if filepath.count(os.path.sep) == 1:
        filepath += 'others' + os.path.sep

    # Date
    filepath += time.strftime('%Y' + os.path.sep)
    # Filename
    filepath += slugify(file) + '.' + ext

    return filepath


class Attachment(TimeStampedUUIDModel):
    DEFAULT_ATTACHMENT, AVATARS, ID_CARD = 'global', 'avatars', 'id_cards'
    AttachmentChoices = ((DEFAULT_ATTACHMENT, 'global'), (AVATARS, 'avatars'),
                         (ID_CARD, 'id_cards'))
    attachment_type = models.CharField(max_length=20,
                                       choices=AttachmentChoices,
                                       default=DEFAULT_ATTACHMENT)
    path = models.FileField(upload_to=content_file_name)
    file_type = models.CharField(max_length=200, blank=True, null=True)
    size = models.IntegerField(null=True, blank=True)
    hash_value = models.CharField(max_length=500,
                                  null=True,
                                  blank=True,
                                  db_index=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "{id} ({filename})".format(id=self.id, filename=self.path.name)

    def save(self, *args, **kwargs):
        mime = MimeTypes()
        self.file_type = mime.guess_type(self.path.name)[0]
        self.name = self.path.name
        self.size = self.path.size
        self.attachment_type = 'global'

        # Calculate hash
        md5hash = hashlib.md5()
        for chunk in self.path.chunks():
            md5hash.update(chunk)
        self.hash_value = md5hash.hexdigest()

        self.path.file.seek(0)
        super(Attachment, self).save()

    # def get_absolute_url(self):
    #     return str(self.path.)

    class Meta:
        ordering = ('created', )
