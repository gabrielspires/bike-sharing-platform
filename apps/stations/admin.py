from django.contrib import admin

from .models import Station


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "city",
        "active",
        "latitude",
        "longitude",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "city",
        "name",
        "active",
        "created_at",
        "updated_at",
    ]
    search_fields = ["city", "name", "active", "station"]
    ordering = ["-updated_at"]
