from django.db import models

from bookit.access.models import User
from bookit.common.models import (TimeStampedEnumeratedUUIDModel,
                                  TimeStampedUUIDModel, Attachment)


class Tags(TimeStampedEnumeratedUUIDModel):
    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created', )


class Language(TimeStampedEnumeratedUUIDModel):
    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created', )


class Event(TimeStampedEnumeratedUUIDModel):
    start_time = models.DateTimeField()
    booking_closes_before = models.IntegerField()
    number_of_seats = models.BigIntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    languages = models.ManyToManyField(Language, related_name='events')
    tags = models.ManyToManyField(Tags, related_name='events')
    image = models.ForeignKey(Attachment,
                              related_name='events',
                              on_delete=models.CASCADE)
    age_limit = models.IntegerField(null=True, blank=True)
    cost_per_person = models.BigIntegerField()
    city = models.TextField()
    terms_and_conditions = models.TextField()
    views_count = models.IntegerField(default=0)
    venue = models.TextField()
    duration = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created', )


class Booking(TimeStampedUUIDModel):
    REGISTRATION_TYPE = (('Self', 'Self'), ('Group', 'Group'),
                         ('Corporate', 'Corporate'), ('Others', 'Others'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registration_type = models.CharField(max_length=20,
                                         choices=REGISTRATION_TYPE,
                                         default='self')
    number_of_tickets = models.IntegerField()

    def __str__(self):
        return "{} {}".format(self.registration_type, self.event.title)

    class Meta:
        ordering = ('created', )
