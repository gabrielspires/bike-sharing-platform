import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.trips.models import Category, Trip
from core.factories import TripFactory, UserFactory

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds the database with Users and Trips"

    def add_arguments(self, parser):
        parser.add_argument(
            "--user-count",
            type=int,
            default=10,
            help="Number of users to create",
        )
        parser.add_argument(
            "--trip-count",
            type=int,
            default=100,
            help="Number of trips to create",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding",
        )

    def handle(self, *args, user_count=10, trip_count=100, clear=False, **options):
        self.stdout.write("Clearing existing data...")

        with transaction.atomic():
            if clear:
                Trip.objects.all().delete()
                User.objects.all().delete()

                self.stdout.write(self.style.WARNING("Existing data cleared."))

            self.stdout.write("Seeding new data...")
            # 1. Create users and categories
            users = UserFactory.create_batch(user_count)
            categories = Category.objects.all()

            # 2. Create trips
            for _ in range(trip_count):
                TripFactory.create(user=random.choice(users), category=random.choice(categories))

        self.stdout.write(self.style.SUCCESS("Successfully seeded 10 users and 50 trips!"))
