import os

from django.db import models


# def appinfo_img_path(instance, filename):
#     return os.path.join("appinfo", str(instance.pk), filename)
#
#
# class AppInfo(models.Model):
#     TYPES = (
#         (0, "none"),
#         (1, "simple"),
#         (2, "simple_dialog_closable"),
#         (3, "simple_dialog"),
#         (4, "critical_alert"),
#     )
#     title = models.CharField(max_length=255)
#     text = models.TextField(blank=True)
#     img = models.ImageField(upload_to=appinfo_img_path, blank=True, default=None, null=True)
#     type = models.IntegerField(choices=TYPES, default=1)


class MobileAppsConfig(models.Model):
    name = models.CharField(max_length=255, default="")

    # ios
    ios_latest_version = models.IntegerField(verbose_name="Последняя IOS версия")
    ios_min_version = models.IntegerField(verbose_name="Минимальная IOS версия")
    ios_app_href = models.CharField(blank=True, verbose_name="Ссылка на приложение IOS", max_length=1000)

    # android
    android_app_latest_version = models.IntegerField(verbose_name="Последняя Android версия")
    android_app_min_version = models.IntegerField(verbose_name="Минимальная Android версия")
    android_app_href = models.CharField(blank=True, verbose_name="Ссылка на приложение Android", max_length=1000)

    actual = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Конфигурация"
        verbose_name_plural = "Конфигурации мобильных приложений"
        ordering = ["-actual", "-id"]

    def __str__(self):
        return self.name if self.name != "" else "#config_" + str(self.id)

    def save(self, *args, **kwargs):
        if self.actual:
            MobileAppsConfig.objects.exclude(id=self.id).update(actual=False)
        if not MobileAppsConfig.objects.exists():
            self.actual = True
        return super(MobileAppsConfig, self).save(*args, **kwargs)


class ServerMaintenance(models.Model):
    title = models.CharField(verbose_name="Причина", max_length=255)
    start = models.DateTimeField(verbose_name="Начало")
    end = models.DateTimeField(verbose_name="Конец")
    description = models.TextField(verbose_name="Описание", blank=True, default="")

    class Meta:
        verbose_name = "Технические работы"
        verbose_name_plural = "Технические работы"
        ordering = ["-start"]
