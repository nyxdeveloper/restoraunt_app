from django.db import models
import os
from pyfcm import FCMNotification
from restoraunt_app.settings import FCM_DJANGO_SETTINGS

push_service = FCMNotification(api_key=FCM_DJANGO_SETTINGS["FCM_SERVER_KEY"])


def menu_img_path(instance, filename):
    return os.path.join("menu", instance.name, filename)


def dish_img_path(instance, filename):
    return os.path.join("dishes", instance.name, filename)


def topping_img_path(instance, filename):
    return os.path.join("toppings", instance.name, filename)


class Menu(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, default="", verbose_name="Описание")
    img = models.ImageField(upload_to=menu_img_path, null=True, default=None, verbose_name="Изображение")
    weight = models.IntegerField(default=1, verbose_name="Позиция на экране")

    def __str__(self): return self.name

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"
        ordering = ["weight"]


class DishKind(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    menu = models.ManyToManyField("menu.Menu", blank=True, related_name="dish_kinds")
    description = models.TextField(blank=True, default="", verbose_name="Описание")

    def __str__(self): return self.name

    class Meta:
        verbose_name = "Вид блюда"
        verbose_name_plural = "Виды блюд"
        ordering = ["name"]


class ToppingKind(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, default="", verbose_name="Описание")

    def __str__(self): return self.name

    class Meta:
        verbose_name = "Вид допинга"
        verbose_name_plural = "Виды допингов"
        ordering = ["name"]


class Dish(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    kind = models.ForeignKey("menu.DishKind", on_delete=models.SET_NULL, default=None, null=True, verbose_name="Вид",
                             related_name="dishes")
    menu = models.ManyToManyField("menu.Menu", blank=True, verbose_name="Меню", related_name="dishes")
    dishes = models.ManyToManyField("menu.Dish", blank=True, verbose_name="Входящие блюда")
    img = models.ImageField(upload_to=dish_img_path, null=True, default=None, verbose_name="Изображение")
    description = models.TextField(blank=True, default="", verbose_name="Описание")
    cost = models.DecimalField(max_digits=9, decimal_places=2, default=1)
    proteins = models.FloatField(verbose_name='Белки', default=0.0, blank=True)
    fats = models.FloatField(verbose_name='Жиры', default=0.0, blank=True)
    carbohydrates = models.FloatField(verbose_name='Углеводы', default=0.0, blank=True)
    cost_aggregated = models.BooleanField(default=False, verbose_name="Стоимость составляется из компонентов")

    def __str__(self): return self.name

    def save(self, *args, **kwargs):
        if self.cost_aggregated:
            cost = self.dishes.aggregate(cost=models.Sum("cost"))["cost"]
            self.cost = cost if cost else 0
        return super(Dish, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
        ordering = ["kind__name"]


class Topping(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    kind = models.ForeignKey("menu.ToppingKind", on_delete=models.SET_NULL, default=None, null=True, verbose_name="Вид",
                             related_name="topings")
    description = models.TextField(blank=True, default="", verbose_name="Описание")
    img = models.ImageField(upload_to=topping_img_path, null=True, default=None, verbose_name="Изображение")
    cost = models.DecimalField(max_digits=9, decimal_places=2, default=1)
    proteins = models.FloatField(verbose_name='Белки', default=0.0, blank=True)
    fats = models.FloatField(verbose_name='Жиры', default=0.0, blank=True)
    carbohydrates = models.FloatField(verbose_name='Углеводы', default=0.0, blank=True)

    def __str__(self): return self.name

    class Meta:
        verbose_name = "Допинг"
        verbose_name_plural = "Допинги"
        ordering = ["name"]


class Order(models.Model):
    STATUSES = (
        ("in_process", "Обрабатывается"),
        ("canceled", "Отменен"),
        ("preparing", "Готовится"),
        ("delivering", "Доставляется"),
        ("is_deliver", "Доставлен"),
        ("completed", "Завершен"),
    )

    TYPES = (
        ("delivery", "Доставка"),
        ("pickup", "Самовывоз"),
        ("on_spot", "На месте"),
    )

    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, default=None)
    toppings = models.ManyToManyField("menu.Topping", verbose_name="Допинги")
    comment = models.TextField(blank=True, verbose_name="Коментарий")
    cost = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    address = models.ForeignKey("accounts.Address", on_delete=models.SET_NULL, null=True, default=None)
    status = models.CharField(max_length=20, choices=STATUSES, default="in_process")
    type = models.CharField(max_length=20, choices=TYPES, default="on_spot")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.pk}"

    def save(self, *args, **kwargs):
        order = Order.objects.filter(id=self.id).first()
        old_status = order.status if order else None
        new_status = self.status
        super(Order, self).save(*args, **kwargs)
        if old_status:
            if new_status != old_status:
                if new_status == "in_process":
                    title = f"Ваш заказ #{self.pk} обрабатывается"
                    message = ""
                elif new_status == "canceled":
                    title = f"Ваш заказ #{self.pk} отменен"
                    message = ""
                elif new_status == "preparing":
                    title = f"Ваш заказ #{self.pk} готовится"
                    message = ""
                elif new_status == "delivering":
                    title = f"Курьер доставляет ваш заказ #{self.pk}"
                    message = ""
                elif new_status == "is_deliver":
                    title = f"Ваш заказ #{self.pk} доставлен. Приятного аппетита!"
                    message = ""
                elif new_status == "completed":
                    title = f"Заказ #{self.pk} завершен!"
                    message = ""
                else:
                    return None
                push_service.notify_topic_subscribers(
                    message_title=title,
                    badge=1,
                    topic_name=str(self.user.pk),
                    message_body=message, sound="default",
                    extra_notification_kwargs={"order_id": self.id})
            else:
                return None
        else:
            title = f"Заказ #{self.pk} успешно создан"
            message = ""
        push_service.notify_topic_subscribers(
            message_title=title,
            badge=1,
            topic_name=str(self.user.pk),
            message_body=message, sound="default",
            extra_notification_kwargs={"order_id": self.id})

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created"]


class OrderPosition(models.Model):
    dish = models.ForeignKey("menu.Dish", on_delete=models.SET_NULL, null=True, default=None)
    dishes = models.ManyToManyField("menu.Dish", verbose_name="Блюда", related_name="complected")
    order = models.ForeignKey("menu.Order", on_delete=models.CASCADE, null=False, related_name="positions")
    count = models.PositiveIntegerField(default=1)

    def __str__(self): return self.dish.name

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"
        ordering = ["dish__name"]
