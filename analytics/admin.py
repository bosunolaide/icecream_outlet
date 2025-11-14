
from django.contrib import admin
from .models import OrderAnalytics
@admin.register(OrderAnalytics)
class OrderAnalyticsAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_id", "total", "created_at")
    search_fields = ("id", "customer_id")
