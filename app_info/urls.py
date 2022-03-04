# reast framework
from rest_framework.routers import DefaultRouter

# локальные импорты
from .views import FAQReadOnnlyViewSet

router = DefaultRouter()

router.register("faq", FAQReadOnnlyViewSet)

urlpatterns = router.urls
