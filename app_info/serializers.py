# rest framework
from rest_framework import serializers

# локальные импорты
from .models import FAQ


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"
