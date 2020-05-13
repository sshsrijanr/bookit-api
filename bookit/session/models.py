from django.db import models

from bookit.access.models import User
from bookit.common.models import (TimeStampedEnumeratedUUIDModel, TimeStampedUUIDModel)


# Create your models here.
class Event(TimeStampedEnumeratedUUIDModel):
    start_time = models.DateTimeField()
    # field to determine closing of booking/Registration in hrs
    booking_closes_before = models.IntegerField()
    number_of_seats = models.BigIntegerField()

    def __str__(self):
        return self.title


class Booking(TimeStampedUUIDModel):
    REGISTRATION_TYPE = (('self', 'self'), ('Group', 'Group'), ('Corporate', 'Corporate'), ('Others', 'Others'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registration_type = models.CharField(max_length=20, choices=REGISTRATION_TYPE, default='self')
    number_of_tickets = models.IntegerField()
