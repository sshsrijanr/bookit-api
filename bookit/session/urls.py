from config import OptionalSlashDefaultRouter
from django.urls import re_path
from .views import (LanguageViewSet, EventViewSet, BookingViewSet, TagViewSet,
                    booking_type_stats, booking_event_stats,
                    monthly_booking_stats)
router = OptionalSlashDefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('languages', LanguageViewSet, basename='languages')
router.register('events', EventViewSet, basename='events')
router.register('bookings', BookingViewSet, basename='bookings')

urlpatterns = [
    re_path('booking-type-stats',
            booking_type_stats,
            name='booking_type_stats'),
    re_path('monthly-booking-stats',
            monthly_booking_stats,
            name='monthly_booking_stats'),
    re_path('event-booking-stats/(?P<event>[^/.]+)/?',
            booking_event_stats,
            name='event_booking_stats')
]

urlpatterns += router.urls