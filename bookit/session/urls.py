from config import OptionalSlashDefaultRouter
from django.urls import re_path
from .views import LanguageViewSet, EventViewSet, BookingViewSet, TagViewSet, booking_type_stats
    # booking_days
router = OptionalSlashDefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('languages', LanguageViewSet, basename='languages')
router.register('events', EventViewSet, basename='events')
router.register('bookings', BookingViewSet, basename='bookings')

urlpatterns = [
    re_path('booking-type-stats', booking_type_stats, name='booking_type_stats'),
    # re_path('booking-days', booking_days, name='booking_days')
]

urlpatterns += router.urls