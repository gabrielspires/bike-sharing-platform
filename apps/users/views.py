from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.trips.models import Trip
from apps.trips.serializers import TripSerializer

from .models import User
from .serializers import UserSerializer


@extend_schema(
    tags=["Users"],
    summary="List users",
    description="Returns all users.",
    responses={200: UserSerializer(many=True)},
)
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(
    tags=["Users"],
    summary="List user trips",
    description="Returns all trips from a user.",
    responses={200: TripSerializer(many=True)},
)
class UserTrips(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = TripSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("pk")
        print(user_id)
        return Trip.objects.filter(user=user_id).select_related("user")
