from django.contrib.auth.models import AbstractUser
from django.db import models

from bookit.common.models import UUIDModel, TimeStampedUUIDModel, Attachment


# Create your models here.

class User(AbstractUser, UUIDModel):
    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Profile(TimeStampedUUIDModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.BigIntegerField(null=True, blank=True)
    id_card = models.ForeignKey(Attachment, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)
