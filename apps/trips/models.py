from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.bikes.models import Bike
from common.models import BaseModel

MIN_TRIP_SCORE = 1
MAX_TRIP_SCORE = 5


class Category(BaseModel):
    class CategoryDescriptions(models.TextChoices):
        T1 = "work", "Work"
        T2 = "exercise", "Exercise"
        T3 = "leisure", "Leisure"
        T4 = "commuting", "Commuting"

    id = models.AutoField(primary_key=True)
    description = models.CharField(
        max_length=255, choices=CategoryDescriptions, default=CategoryDescriptions.T2, unique=True
    )

    def __str__(self):
        return self.CategoryDescriptions(self.description).label

    class Meta:
        verbose_name_plural = "Categories"


class Trip(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="trips", db_index=True
    )
    bike = models.ForeignKey(
        Bike, on_delete=models.DO_NOTHING, related_name="trips", db_index=True, default=None
    )
    finished_at = models.DateTimeField(blank=True, null=True, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="trips")
    score = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(MIN_TRIP_SCORE), MaxValueValidator(MAX_TRIP_SCORE)],
    )
