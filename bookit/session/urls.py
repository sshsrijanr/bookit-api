from config import OptionalSlashDefaultRouter
from .views import LanguageViewSet, EventViewSet, BookingViewSet, TagViewSet
router = OptionalSlashDefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('languages', LanguageViewSet, basename='languages')
router.register('events', EventViewSet, basename='events')
router.register('bookings', BookingViewSet, basename='bookings')

urlpatterns = []

urlpatterns += router.urls