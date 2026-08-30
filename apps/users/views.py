from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.renderers import JSONRenderer

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
    renderer_classes = [JSONRenderer]
