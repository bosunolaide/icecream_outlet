from rest_framework.routers import DefaultRouter
from .views import FlavourViewSet

router = DefaultRouter()
router.register(r"", FlavourViewSet, basename="flavour")

urlpatterns = router.urls
