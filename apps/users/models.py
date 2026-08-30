from django.db import models

from common.models import BaseUser


class User(BaseUser):
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
