from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Station
from .serializers import StationSerializer


@extend_schema(
    tags=["Stations"],
    summary="List stations",
    description="Returns all stations.",
    responses={200: StationSerializer(many=True)},
)
class StationListView(ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Station.objects.all()
    serializer_class = StationSerializer
