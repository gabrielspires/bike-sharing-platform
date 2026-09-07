from django.contrib import admin

from .models import Category, Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "category",
        "created_at",
        "updated_at",
        "finished_at",
        "score",
    ]
    list_filter = ["category", "score", "created_at", "updated_at", "finished_at"]
    search_fields = ["category", "user", "score"]
    ordering = ["-updated_at"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "description",
        "id",
    ]
    ordering = ["id"]
