# rest framework
from rest_framework.viewsets import ReadOnlyModelViewSet

# локальные импорты
from .models import FAQ
from .serializers import FAQSerializer


class FAQReadOnnlyViewSet(ReadOnlyModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

