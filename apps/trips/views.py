import logging

from django.db import transaction
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.bikes.models import Bike
from apps.users.models import User

from .models import Category, Trip
from .serializers import CategorySerializer, CreateTripSerializer, FinishTripSerializer, TripSerializer
from .tasks import finish_trip

logger = logging.getLogger("django")


@extend_schema(
    tags=["Trips"],
    summary="List trips",
    description="Returns all trips.",
    responses={200: TripSerializer(many=True)},
)
class TripList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = TripSerializer

    def get_queryset(self):
        user = User.objects.filter(id=self.request.user.pk).first()
        if user and (user.is_staff or user.is_superuser):
            # Admins can list all Trips
            return Trip.objects.select_related("user", "category").all()

        # Normal users can only see their own Trips
        return Trip.objects.filter(user=self.request.user).select_related("user", "category")


@extend_schema(
    tags=["Trips"],
    summary="List categories",
    description="Returns all categories.",
    responses={200: CategorySerializer(many=True)},
)
class CategoryList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema(
    tags=["Trips"],
    summary="Starts a trip",
    description="Starts a trip and change the status of the bike used.",
    responses={200: TripSerializer},
)
class StartTrip(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = CreateTripSerializer

    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user).select_related("user", "category")

    def perform_create(self, serializer: CreateTripSerializer):
        with transaction.atomic():
            bike = Bike.objects.filter(id=serializer.validated_data.get("bike").id).get()
            start_station = bike.station

            bike.status = Bike.BikeStatus.IN_USE
            bike.station = None

            serializer.save(user=self.request.user, start_station=start_station)
            bike.save()

            logger.info(
                "Trip started.",
                extra={
                    "extra_data": {
                        "user_id": self.request.user,
                        "bike_id": bike.id,
                        "start_station": start_station,
                        "status_code": status.HTTP_200_OK,
                    }
                },
            )


@extend_schema(
    tags=["Trips"],
    summary="Finish a trip",
    description="Finishes a trip and trigger the email sending task.",
    responses={200: TripSerializer},
)
class FinishTrip(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = FinishTripSerializer

    http_method_names = ["patch"]

    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user).select_related("user", "category")

    def perform_update(self, serializer: FinishTripSerializer):
        with transaction.atomic():
            trip_id = self.kwargs.get("pk")
            trip = Trip.objects.filter(id=trip_id).get()

            if trip.finished_at:
                raise ValidationError(
                    {
                        "detail": "This trip has already been completed.",
                        "error_code": "TRIP_ALREADY_FINISHED",
                    }
                )

            finish_station = serializer.validated_data.get("finish_station")

            bike_id = trip.bike.id

            bike = Bike.objects.filter(id=bike_id).get()
            bike.status = Bike.BikeStatus.AVAILABLE
            bike.station = finish_station
            bike.save()

            trip = serializer.save(finish_station=finish_station, finished_at=timezone.now())

            finish_trip.delay(trip.id)

            logger.info(
                "Trip finished.",
                extra={
                    "extra_data": {
                        "user_id": self.request.user.pk,
                        "bike_id": bike.id,
                        "start_station": trip.start_station.pk,
                        "finish_station": finish_station.pk,
                        "status_code": status.HTTP_200_OK,
                    }
                },
            )
