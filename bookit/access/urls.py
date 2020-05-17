from config import OptionalSlashDefaultRouter
from .views import UserViewSet
router = OptionalSlashDefaultRouter()

router.register('users', UserViewSet, basename='users')

urlpatterns = []

urlpatterns += router.urls