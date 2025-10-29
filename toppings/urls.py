from rest_framework.routers import DefaultRouter
from .views import ToppingViewSet

router = DefaultRouter()
router.register(r"", ToppingViewSet, basename="topping")

urlpatterns = router.urls
