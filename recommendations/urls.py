from django.urls import path
from .views import RecommendFlavoursView

urlpatterns = [
    path("flavours/", RecommendFlavoursView.as_view(), name="recommend-flavours"),
]