from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.users.models import User

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
    summary="Finish a trip",
    description="Finishes a trip and trigger the email sending task.",
    responses={200: TripSerializer},
)
class FinishTrip(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = TripSerializer

    http_method_names = ["patch"]

    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user).select_related("user", "category")

    def perform_update(self, serializer: TripSerializer):
        trip = serializer.save(finished_at=timezone.now())
        finish_trip.delay(trip.id)
