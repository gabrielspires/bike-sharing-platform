from django.db import models

from apps.stations.models import Station
from common.models import BaseModel


class Bike(BaseModel):
    class BikeType(models.TextChoices):
        ELECTRIC = "electric", "Electric"
        MECHANIC = "mechanic", "Mechanic"

    class BikeStatus(models.TextChoices):
        AVAILABLE = "available", "Available"
        IN_USE = "in_use", "In use"
        MAINTENANCE = "maintenance", "Maintenance"
        INACTIVE = "inactive", "Inactive"
        UNKNOWN = "unknown", "Unknown"

    code = models.CharField(max_length=254, blank=False, null=False)
    status = models.CharField(max_length=254, choices=BikeStatus, default=BikeStatus.UNKNOWN)
    type = models.CharField(max_length=254, choices=BikeType, default=BikeType.MECHANIC)
    station = models.ForeignKey(Station, on_delete=models.PROTECT, related_name="bikes", db_index=True)

    def __str__(self):
        return self.code
