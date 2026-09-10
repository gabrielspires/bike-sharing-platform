from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from common.models import BaseModel


class Station(BaseModel):
    name = models.CharField(max_length=254, blank=False, unique=True)
    latitude = models.DecimalField(
        max_digits=8, decimal_places=6, validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.DecimalField(
        max_digits=8, decimal_places=6, validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    active = models.BooleanField(default=True)
    city = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return self.name
