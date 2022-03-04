# rest framework
from rest_framework.routers import DefaultRouter

# локальные импорты
from .views import MenuReadOnlyViewSet
from .views import DishKindReadOnlyViewSet
from .views import ToppingKindReadOnlyViewSet
from .views import ToppingReadOnlyViewSet
from .views import DishReadOnlyViewSet
from .views import OrderViewSet

router = DefaultRouter()

router.register("menu", MenuReadOnlyViewSet)
router.register("dish_kinds", DishKindReadOnlyViewSet)
router.register("topping_kinds", ToppingKindReadOnlyViewSet)
router.register("toppings", ToppingReadOnlyViewSet)
router.register("dishes", DishReadOnlyViewSet)
router.register("orders", OrderViewSet)

urlpatterns = router.urls
