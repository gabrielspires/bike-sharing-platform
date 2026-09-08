from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer

from .models import Category, Trip
from .serializers import CategorySerializer, TripSerializer
from .tasks import finish_trip


@extend_schema(
    tags=["Trips"],
    summary="List trips",
    description="Returns all trips.",
    responses={200: TripSerializer(many=True)},
)
class TripList(generics.ListAPIView):
    queryset = Trip.objects.select_related("user", "category").all()
    serializer_class = TripSerializer
    renderer_classes = [JSONRenderer]


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
    renderer_classes = [JSONRenderer]


@extend_schema(
    tags=["Trips"],
    summary="Finish a trip",
    description="Finishes a trip and trigger the email sending task.",
    responses={200: TripSerializer},
)
class FinishTrip(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Trip.objects.select_related("user", "category").all()
    serializer_class = TripSerializer
    renderer_classes = [JSONRenderer]

    http_method_names = ["patch"]

    def perform_update(self, serializer):
        trip = serializer.save(finished_at=timezone.now())
        finish_trip.delay(trip.id)
