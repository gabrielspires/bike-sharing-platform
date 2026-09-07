import random
from datetime import datetime, timedelta

import factory
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.trips.models import MAX_TRIP_SCORE, MIN_TRIP_SCORE, Category, Trip

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_staff = False
    is_active = True
    is_superuser = False
    password = factory.Faker(
        "password", length=16, special_chars=True, digits=True, upper_case=True, lower_case=True
    )

    @classmethod
    def _setup_next_sequence(cls):
        return User.objects.count()

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


def get_random_finished_time():
    random_minutes = random.randint(0, 120)
    return timezone.now() + timedelta(minutes=random_minutes)


def get_random_updated_time(start: datetime | None = None):
    random_minutes = random.randint(120, 120)
    return timezone.now() + timedelta(minutes=random_minutes)


class TripFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Trip

    user = factory.SubFactory(UserFactory)
    category = random.choice(Category.objects.all())
    score = factory.Faker("random_int", min=MIN_TRIP_SCORE, max=MAX_TRIP_SCORE)
    finished_at = factory.LazyAttribute(lambda _: timezone.now() + timedelta(minutes=random.randint(0, 120)))
    updated_at = factory.LazyAttribute(lambda o: o.finished_at + timedelta(minutes=random.randint(120, 240)))
