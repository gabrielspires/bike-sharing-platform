from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from common.models import BaseModel

MIN_TRIP_SCORE = 1
MAX_TRIP_SCORE = 5


class Category(BaseModel):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = "Categories"


class Trip(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="trips", db_index=True
    )
    finished_at = models.DateTimeField(blank=True, null=True, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="trips")
    score = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(MIN_TRIP_SCORE), MaxValueValidator(MAX_TRIP_SCORE)],
    )
