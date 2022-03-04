# Внутренние импорты
import os
import uuid

# Импорты django
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Sum
from django.db import transaction


def avatar_filepath(instance, filename):
    return os.path.join("users", str(instance.pk), filename)


class UserManager(BaseUserManager):
    @transaction.atomic
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        try:
            user = self.model(username=username, **extra_fields)
            user.set_password(password)
            user.save()
            return user
        except:
            raise

    def create_user(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, default="", blank=True, unique=True)

    # chars
    phone = models.CharField(verbose_name='Номер телефона', null=True, blank=True, max_length=50, default=None)
    name = models.CharField(max_length=50, blank=True, default=None, null=True)

    points = models.PositiveIntegerField(default=0)

    # files
    # avatar = models.ImageField(upload_to=avatar_filepath, blank=True, null=True, default=None)

    # booleans
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # dates
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name if self.name else str(self.phone)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = str(self.pk)
        return super(User, self).save(*args, **kwargs)


class Address(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, default=None,
                             related_name="addresses")
    address = models.TextField(verbose_name="Адрес")
    default = models.BooleanField(default=False)
    longitude = models.DecimalField(max_digits=23, decimal_places=17)
    latitude = models.DecimalField(max_digits=23, decimal_places=17)

    def __str__(self):
        return self.address

    def save(self, *args, **kwargs):
        if self.default:
            Address.objects.filter(user=self.user).exclude(id=self.id).update(default=False)
        if not Address.objects.filter(user=self.user).exclude(id=self.id).exists():
            self.default = True
        return super(Address, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"
        ordering = ["-default", "-id"]


class OTC(models.Model):
    key = models.CharField(max_length=100, primary_key=True)
    code = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Одноразовый код"
        verbose_name_plural = "Одноразовые коды"

    def __str__(self):
        return self.code
