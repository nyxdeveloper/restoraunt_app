# rest framework
from rest_framework import serializers

# локальные импорты
from .models import Menu
from .models import DishKind
from .models import ToppingKind
from .models import Topping
from .models import Dish
from .models import OrderPosition
from .models import Order


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


class DishKindSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishKind
        fields = "__all__"


class ToppingKindSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToppingKind
        fields = "__all__"


class ToppingSerializer(serializers.ModelSerializer):
    _kind = serializers.StringRelatedField(source="kind")
    cost = serializers.FloatField()

    class Meta:
        model = Topping
        fields = "__all__"


class DishSerializer(serializers.ModelSerializer):
    _kind = serializers.StringRelatedField(source="kind")
    cost = serializers.FloatField()

    class Meta:
        model = Dish
        fields = "__all__"


class OrderPositionSerializer(serializers.ModelSerializer):
    class OrderPositionDishSerializer(serializers.Serializer):
        id = serializers.CharField(read_only=True)
        name = serializers.CharField(read_only=True)
        cost = serializers.FloatField(read_only=True)

    _dishes = OrderPositionDishSerializer(read_only=True, source="dishes", many=True)

    class Meta:
        model = OrderPosition
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class OrderUserSerializer(serializers.Serializer):
        id = serializers.CharField(read_only=True)
        name = serializers.CharField(read_only=True)
        points = serializers.IntegerField(read_only=True)

    class OrderTopingSerializer(serializers.Serializer):
        id = serializers.CharField(read_only=True)
        name = serializers.CharField(read_only=True)
        cost = serializers.FloatField(read_only=True)

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    _user = OrderUserSerializer(read_only=True, source="user")
    _toppings = OrderTopingSerializer(read_only=True, source="toppings", many=True)
    _positions = OrderPositionSerializer(read_only=True, source="positions", many=True)
    _address = serializers.SlugRelatedField(read_only=True, slug_field="address", source="address")
    cost = serializers.FloatField()

    class Meta:
        model = Order
        fields = "__all__"


class OrderCreateSerializer(serializers.ModelSerializer):
    class CurrentUserAddressDefault:
        requires_context = True

        def __call__(self, serializer_field):
            return serializer_field.context['request'].user.addresses.get(default=True)

        def __repr__(self):
            return '%s()' % self.__class__.__name__

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = [
            "user", "comment", "toppings", "address", "type"
        ]
