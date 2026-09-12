from django.contrib import admin

from .models import Category, Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "bike",
        "category",
        "score",
        "created_at",
        "updated_at",
        "finished_at",
    ]
    list_filter = ["category", "score", "created_at", "updated_at", "finished_at"]
    search_fields = ["category", "user", "bike", "score"]
    ordering = ["-updated_at"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "description",
        "id",
    ]
    ordering = ["id"]
