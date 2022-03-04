# django
from django.db import transaction
from django.db.models import Sum

# rest framework
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

# локальные импорты
from .models import Menu
from .models import DishKind
from .models import ToppingKind
from .models import Topping
from .models import Dish
from .models import OrderPosition
from .models import Order

from .exceptions import EmptyOrder
from .exceptions import DishNotFound

from .serializers import MenuSerializer
from .serializers import DishKindSerializer
from .serializers import ToppingKindSerializer
from .serializers import ToppingSerializer
from .serializers import DishSerializer
from .serializers import OrderPositionSerializer
from .serializers import OrderSerializer
from .serializers import OrderCreateSerializer

# itpwlib
from itpwlib.filters import query_params_filter


class MenuReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    # pagination_class = PageNumberPagination
    permission_classes = [AllowAny, ]


class DishKindReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = DishKind.objects.all()
    serializer_class = DishKindSerializer
    # pagination_class = PageNumberPagination
    permission_classes = [AllowAny, ]
    filterset_key_fields = ["menu"]
    filterset_char_fields = ["name"]

    def filter_queryset(self, queryset):
        queryset = super(DishKindReadOnlyViewSet, self).filter_queryset(queryset)
        queryset = query_params_filter(self.request, queryset, self.filterset_key_fields, self.filterset_char_fields)
        return queryset


class ToppingKindReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = ToppingKind.objects.all()
    serializer_class = ToppingKindSerializer
    # pagination_class = PageNumberPagination
    permission_classes = [AllowAny, ]


class ToppingReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Topping.objects.all()
    serializer_class = ToppingSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny, ]

    filterset_key_fields = ["kind"]
    filterset_char_fields = ["name"]

    def filter_queryset(self, queryset):
        queryset = super(ToppingReadOnlyViewSet, self).filter_queryset(queryset)
        queryset = query_params_filter(self.request, queryset, self.filterset_key_fields, self.filterset_char_fields)
        return queryset


class DishReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny, ]

    filterset_key_fields = ["kind", "menu"]
    filterset_char_fields = ["name"]

    def filter_queryset(self, queryset):
        queryset = super(DishReadOnlyViewSet, self).filter_queryset(queryset)
        queryset = query_params_filter(self.request, queryset, self.filterset_key_fields, self.filterset_char_fields)
        return queryset


class OrderViewSet(GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated, ]
    filterset_key_fields = []
    filterset_char_fields = []

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def filter_queryset(self, queryset):
        queryset = super(OrderViewSet, self).filter_queryset(queryset)
        queryset = query_params_filter(self.request, queryset, self.filterset_key_fields, self.filterset_char_fields)
        return queryset

    def get_serializer_class(self):
        if self.action == "create_order":
            return OrderCreateSerializer
        return super(OrderViewSet, self).get_serializer_class()

    @transaction.atomic
    @action(methods=["POST"], detail=False)
    def create_order(self, request):
        order_data = request.data
        positions = order_data["positions"]
        if not len(positions):
            raise EmptyOrder
        serializer = self.get_serializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        order = serializer.instance
        for position in positions:
            dish = Dish.objects.filter(id=position["dish"]).first()
            if not dish:
                raise DishNotFound(f"Блюдо с id {position['dish']} не найдено")
            new_position = order.positions.create(
                dish=dish,
                count=position["count"]
            )
            new_position.dishes.add(*dish.dishes.values_list("id", flat=True))
            order.cost = order.cost + new_position.dish.cost * new_position.count
        toppings_cost = order.toppings.aggregate(cost=Sum("cost"))["cost"]
        order.cost = order.cost + toppings_cost if toppings_cost else 0
        order.save()

        response_serializer = self.serializer_class(order)
        return Response(response_serializer.data, status=200)
