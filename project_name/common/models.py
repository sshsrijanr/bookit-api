import uuid
from django.db import models

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