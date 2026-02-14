from django.urls import path
from .views import FlavourRecommendationsAPIView

urlpatterns = [
    path("flavours/", FlavourRecommendationsAPIView.as_view(), name="recommend-flavours"),
]
