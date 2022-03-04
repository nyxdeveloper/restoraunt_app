# внутренние импорты
import random
import requests
import re
import jwt

# django
from django.contrib.auth import user_logged_in

# локальные импорты
from .models import OTC
from .serializers import UserSerializer
from .exceptions import InvalidPhone

# импорты проекта
from restoraunt_app import settings

# сторонние импорты
from rest_framework_jwt.serializers import jwt_payload_handler


def clean_phone(phone):
    clear_phone = re.findall(r"\d+", phone)[0]
    if clear_phone.startswith("8"):
        clear_phone = re.sub("8", "7", clear_phone, 1)
    return clear_phone


def create_otc(login):
    code = str(random.sample(range(10 ** (5 - 1), 10 ** 5), 1)[0])
    OTC.objects.create(key=login, code=code)
    return code


def send_otc(phone):
    if OTC.objects.filter(key=phone).exists():
        OTC.objects.get(key=phone).delete()
    if settings.DEBUG:
        OTC.objects.create(key=phone, code="1111")
        return {"detail": "Код отправлен"}
    code = create_otc(phone)
    url = f'{settings.SMS_SEND_URL}?text={code}&number={phone}&sign={settings.SMS_SIGN_DEFAULT}'
    resp = requests.request(method='GET', url=url)
    if resp.status_code != 200:
        raise InvalidPhone
    return {"detail": f"Сообщение с кодом отправлено по номеру {phone}"}


def get_auth_payload(user, request):
    try:
        payload = jwt_payload_handler(user)
        token = jwt.encode(payload, settings.SECRET_KEY)
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        user_data = UserSerializer(user).data
        if OTC.objects.filter(key=user.phone).exists():
            OTC.objects.get(key=user.phone).delete()
        return {"token": token, "user": user_data}
    except Exception as e:
        raise e

