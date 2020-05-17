from django.urls import re_path
from config import OptionalSlashDefaultRouter
from .views import AttachmentViewSet
urlpatterns = []

router = OptionalSlashDefaultRouter()

router.register(r'attachments', AttachmentViewSet, basename='attachments')


urlpatterns += router.urls