# rest framework
from rest_framework import serializers

from .models import User
from .models import Address


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "phone",
            "name",
            "points",
            "is_staff",
            "is_superuser",
            "date_joined"
        ]


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()

    class Meta:
        model = Address
        fields = "__all__"
