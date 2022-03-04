# rest framework
from rest_framework.exceptions import APIException


class EmptyOrder(APIException):
    status_code = 400
    default_detail = "Нельзя создать пустой заказ"


class DishNotFound(APIException):
    status_code = 404
    default_detail = "Блюдо не найдено"
