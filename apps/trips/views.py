from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.renderers import JSONRenderer

from .models import Category, Trip
from .serializers import CategorySerializer, TripSerializer


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
    tags=["Categories"],
    summary="List categories",
    description="Returns all categories.",
    responses={200: CategorySerializer(many=True)},
)
class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = [JSONRenderer]
