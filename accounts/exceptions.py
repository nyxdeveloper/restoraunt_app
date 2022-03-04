# rest framework
from rest_framework.exceptions import APIException


class InvalidOTC(APIException):
    status_code = 400
    default_detail = "Невалидный одноразовый код"


class InvalidLogin(APIException):
    status_code = 400
    default_detail = "Невалидный логин"


class InvalidPhone(InvalidLogin):
    default_detail = "Невалидный номер телефона"


class InvalidEmail(InvalidLogin):
    default_detail = "Невалидный Email"


class TooManyReports(APIException):
    status_code = 403
    default_detail = "Слишком много репортов"
