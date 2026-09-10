from django.contrib import admin

from .models import Bike


@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "status",
        "type",
        "station",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "status",
        "type",
        "station",
        "created_at",
        "updated_at",
    ]
    search_fields = ["status", "type", "station"]
    ordering = ["-updated_at"]
