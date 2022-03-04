from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import MobileAppsConfig
from .models import ServerMaintenance


class CustomMobileAppsConfigAdmin(ModelAdmin):
    model = MobileAppsConfig
    list_display = ("name", "actual")
    fieldsets = (
        (None, {'fields': ("name",)}),
        ("Версии IOS", {'fields': (
            ("ios_latest_version", "ios_min_version", "ios_app_href"),
        )}),
        ("Версии Android", {'fields': (
            ("android_app_latest_version", "android_app_min_version", "android_app_href"),
        )}),
        ("Дополнительно", {'fields': (
            "actual",
        )}),
    )
    add_fieldsets = (
        (None, {'fields': ("name",)}),
        ("Версии IOS", {'fields': (
            ("ios_latest_version", "ios_min_version", "ios_app_href"),
        )}),
        ("Версии Android", {'fields': (
            ("android_app_latest_version", "android_app_min_version", "android_app_href"),
        )}),
        ("Дополнительно", {'fields': (
            "actual",
        )}),
    )
    list_filter = ["actual", ]
    search_fields = ("name",)
    ordering = ("name", "actual",)


class CustomServerMaintenanceAdmin(ModelAdmin):
    model = ServerMaintenance
    list_display = ("title", "start", "description")
    fieldsets = (
        # (None, {'fields': ("user", "driver", "address",)}),
        ("Инфо", {'fields': (
            ("title", "description",),
        )}),
        ("Время", {'fields': (
            ("start", "end",),
        )}),
    )
    add_fieldsets = (
        # (None, {'fields': ("user", "driver", "address",)}),
        ("Инфо", {'fields': (
            ("title", "description",),
        )}),
        ("Время", {'fields': (
            ("start", "end",),
        )}),
    )
    search_fields = ("title",)
    ordering = ("title", "start", "description",)


admin.site.register(ServerMaintenance, CustomServerMaintenanceAdmin)
admin.site.register(MobileAppsConfig, CustomMobileAppsConfigAdmin)
