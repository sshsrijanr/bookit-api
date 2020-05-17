from django.contrib import admin
from .models import Attachment


# Register your models here.
@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
