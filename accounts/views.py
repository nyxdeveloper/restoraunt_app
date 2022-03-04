import datetime

# rest framework
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# django
from django.db import transaction
from django.utils import timezone

# локальные импорты
from .models import User
from .models import OTC
from .models import Address
from .exceptions import InvalidOTC
from .serializers import UserSerializer
from .serializers import AddressSerializer
from .services import clean_phone
from .services import get_auth_payload
from .services import send_otc

# импорты проекта
from restoraunt_app.settings import APP_ROOT_URL
from restoraunt_app.settings import MEDIA_URL
from restoraunt_app.settings import DEFAULT_NEED_UPDATE_IMG
from restoraunt_app.settings import DEFAULT_SERVER_MAINTENANCE_IMG

# импорты приложений
from configurations.models import MobileAppsConfig
from configurations.models import ServerMaintenance


class AuthenticationViewSet(GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    @transaction.atomic
    @action(methods=["POST"], detail=False)
    def phone_auth(self, request):
        phone = request.data.get("phone")
        otc = request.data.get("otc")

        if not phone:
            return Response({"detail": "Укажите телефон"}, status=400)

        phone = clean_phone(phone)

        if otc:
            if OTC.objects.filter(key=phone, code=otc).exists():
                try:
                    return Response(get_auth_payload(self.get_queryset().get(phone=phone), request))
                except User.DoesNotExist:
                    return Response(get_auth_payload(User.objects.create(phone=phone), request))
            raise InvalidOTC
        return Response(send_otc(phone))


class ProfileViewSet(GenericViewSet, RetrieveModelMixin):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["GET"], detail=False)
    def profile(self, request):
        return Response(self.get_serializer(request.user).data)

    @action(methods=["PUT"], detail=False)
    def change_name(self, request):
        request.user.name = request.data.get("name")
        request.user.save()
        return Response(self.get_serializer(request.user).data, status=200)

    @action(methods=["PUT"], detail=False)
    def change_phone(self, request):
        otc = request.data.get("otc")
        phone = clean_phone(request.data.get("phone"))
        if not phone:
            return Response({"detail": "Укажите телефон"}, status=400)
        if not otc:
            return Response(send_otc(phone))
        if OTC.objects.filter(code=otc, key=phone).exists():
            request.user.phone = phone
            request.user.save()
            return Response(get_auth_payload(request.user, request))
        else:
            raise InvalidOTC

    @action(methods=["DELETE"], detail=False)
    def delete_account(self, request):
        request.user.phone = request.user.pk
        request.user.password = request.user.pk
        request.user.name = "DELETED"
        request.user.is_active = False
        request.user.save()
        return Response(status=204)

    @action(methods=["GET"], detail=False)
    def alerts(self, request):
        os_list = ["ios", "android"]

        version = request.query_params.get("version")
        os = request.query_params.get("os")
        app = request.query_params.get("app")

        if os not in os_list:
            return Response({"detail": "Недопустимый ключ"}, status=400)

        alerts = {
            "none": 0,
            "simple": 1,
            "simple_dialog_closable": 2,
            "simple_dialog": 3,
            "critical_alert": 4
        }

        alert = {
            "type": alerts["none"],
            "title": None,
            "text": None,
            "img": None,
            "buttons": []
        }

        need_update_urgently_titles = {
            "ru": "Ваша версия приложения не поддерживается",
        }

        need_update_titles = {
            "ru": "Вышла более новая версия приложения",
        }

        server_maintenance_soon_titles = {
            "ru": "Скоро технические работы",
        }

        need_update_urgently_texts = {
            "ru": "Версия вашего приложения слишком сильно устарела. Для дальнейшей работы требуется обновление",
        }

        need_update_texts = {
            "ru": "Мы сделали приложение еще быстрее и удобнее! Скорее обновитесь, чтобы пользоваться самыми новыми функциями!",
        }

        server_maintenance_soon_texts = {
            "ru": "Мы стараемся ради того, чтобы вы с комфортом пользовались приложением. Технические работы запланированы на {0}",
        }

        update_button_titles = {
            "ru": "Обновить приложение",
        }

        ok_buttons_titles = {
            "ru": "Ок",
        }

        close_buttons_titles = {
            "ru": "Закрыть",
        }

        need_update_img = APP_ROOT_URL + MEDIA_URL + DEFAULT_NEED_UPDATE_IMG
        server_maintenance_img = APP_ROOT_URL + MEDIA_URL + DEFAULT_SERVER_MAINTENANCE_IMG

        version = int(version) if version else 0

        config = MobileAppsConfig.objects.get(actual=True)

        # чекапы
        need_update = False
        if os == "ios":
            need_update = config.ios_latest_version > version
        elif os == "android":
            need_update = config.android_app_latest_version > version

        need_update_urgently = False
        if os == "ios":
            need_update_urgently = config.ios_min_version > version
        elif os == "android":
            need_update_urgently = config.android_app_min_version > version

        server_maintenance_soon = False
        server_maintenance = None
        if ServerMaintenance.objects.filter(start__gt=timezone.now()):
            server_maintenance = ServerMaintenance.objects.filter(start__gt=timezone.now()).order_by("start").first()
            server_maintenance_soon = server_maintenance.start < timezone.now() + datetime.timedelta(hours=24)

        locale = "ru"
        locale = locale if locale and locale != "" else request.user.locale

        """
        1. Обязательное обновление
        4. Предупреждение о технических работах
        5. Необязательное обновление
        """

        if need_update_urgently:
            if os == "ios":
                app_href = config.ios_app_href
            elif os == "android":
                app_href = config.android_app_href
            else:
                app_href = None
            alert["type"] = alerts["simple_dialog"]
            alert["title"] = need_update_urgently_titles[locale]
            alert["text"] = need_update_urgently_texts[locale]
            alert["img"] = need_update_img
            alert["buttons"] = [
                {"title": update_button_titles[locale], "action": "link:" + app_href, "main": True}
            ]
            return Response(alert)
        elif server_maintenance_soon:
            alert["type"] = alerts["simple_dialog_closable"]
            alert["title"] = server_maintenance_soon_titles[locale]
            alert["text"] = server_maintenance_soon_texts[locale].format(
                server_maintenance.start.strftime("%d.%m.%Y %H:%M"))
            alert["img"] = server_maintenance_img
            alert["buttons"] = [
                {"title": ok_buttons_titles[locale], "action": "close:", "main": True},
            ]
            return Response(alert)
        elif need_update:
            if os == "ios":
                app_href = config.ios_app_href
            elif os == "android":
                app_href = config.android_app_href
            else:
                app_href = None
            alert["type"] = alerts["simple_dialog_closable"]
            alert["title"] = need_update_titles[locale]
            alert["text"] = need_update_texts[locale]
            alert["img"] = need_update_img
            alert["buttons"] = [
                {"title": update_button_titles[locale], "action": "link:" + app_href, "main": True},
            ]
            return Response(alert)
        return Response(alert)


class AddressesViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated, ]

    @action(methods=["POSt"], detail=True)
    def set_default(self, request, pk):
        instance = self.get_object()
        instance.default = not instance.default
        instance.save()
        return Response({"detail": "Адрес по умолчанию изменен"}, status=200)
