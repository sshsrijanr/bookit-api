from django.contrib import admin
from .models import Event, Booking
# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')