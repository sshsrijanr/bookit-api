from config import OptionalSlashDefaultRouter
from .views import LanguageViewSet, EventViewSet, BookingViewSet
router = OptionalSlashDefaultRouter()

router.register('languages', LanguageViewSet, basename='languages')
router.register('events', EventViewSet, basename='events')
router.register('bookings', BookingViewSet, basename='bookings')

urlpatterns = []

urlpatterns += router.urls