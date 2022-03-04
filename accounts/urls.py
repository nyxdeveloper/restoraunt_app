# rest framework
from rest_framework.routers import DefaultRouter

# локальные импорты
from .views import AuthenticationViewSet
from .views import ProfileViewSet
from .views import AddressesViewSet

router = DefaultRouter()

router.register("auth", AuthenticationViewSet)
router.register("profile", ProfileViewSet)
router.register("addresses", AddressesViewSet)

urlpatterns = router.urls
