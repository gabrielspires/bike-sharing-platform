from rest_framework import serializers

from apps.users.serializers import UserSerializer

from .models import Category, Trip


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "description",
        ]


class TripSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Trip
        fields = [
            "id",
            "user",
            "category",
            "created_at",
            "updated_at",
            "finished_at",
            "score",
        ]
