from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer

from .models import Bike
from .serializers import BikeSerializer


@extend_schema(
    tags=["Bikes"],
    summary="List all bikes",
    description="Returns all bikes.",
    responses={200: BikeSerializer(many=True)},
)
class BikeListView(ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Bike.objects.prefetch_related("station").all()
    serializer_class = BikeSerializer
    renderer_classes = [JSONRenderer]
