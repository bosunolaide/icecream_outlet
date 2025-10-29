from django.contrib import admin
from .models import Topping

@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name",)
