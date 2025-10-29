from django.contrib import admin
from .models import Flavour

@admin.register(Flavour)
class FlavourAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name",)
