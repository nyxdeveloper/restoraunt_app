# django
from django.contrib import admin
from .models import Menu
from .models import DishKind
from .models import ToppingKind
from .models import Topping
from .models import Dish
from .models import OrderPosition
from .models import Order


class OrderPositionInline(admin.StackedInline):
    model = OrderPosition
    fk_name = "order"
    extra = 0


class CustomMenuAdmin(admin.ModelAdmin):
    model = Menu
    list_display = ("id", "name", "weight", "description")
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ("name", "weight", "description", "img")
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                "name", "weight", "description", "img"
            )}
         ),
    )
    search_fields = ("name", "description")
    ordering = ("id", "name", "weight", "description")


class CustomDishKindAdmin(admin.ModelAdmin):
    model = DishKind
    list_display = ("id", "name", "description")
    list_filter = ("menu",)
    fieldsets = (
        (None, {
            'fields': ("name", "menu", "description")
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                "name", "menu", "description"
            )}
         ),
    )
    search_fields = ("name", "description")
    ordering = ("id", "name", "description")


class CustomToppingKindAdmin(admin.ModelAdmin):
    model = ToppingKind
    list_display = ("id", "name", "description")
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ("name", "description")
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                "name", "description"
            )}
         ),
    )
    search_fields = ("name", "description")
    ordering = ("id", "name", "description")


class CustomToppingAdmin(admin.ModelAdmin):
    model = Topping
    list_display = ("id", "name", "kind", "cost", "proteins", "fats", "carbohydrates", "description")
    list_filter = ("kind",)
    fieldsets = (
        (None, {
            'fields': ("name", "kind", "cost", "proteins", "fats", "carbohydrates", "description", "img")
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                "name", "kind", "cost", "proteins", "fats", "carbohydrates", "description", "img"
            )}
         ),
    )
    search_fields = ("name", "kind__name", "description")
    ordering = ("id", "name", "kind", "cost", "proteins", "fats", "carbohydrates", "description")


class CustomDishAdmin(admin.ModelAdmin):
    model = Dish
    list_display = ("id", "name", "kind", "cost", "proteins", "fats", "carbohydrates", "description")
    list_filter = ("kind",)
    fieldsets = (
        (None, {
            'fields': ("name", "menu", "kind", "cost", "cost_aggregated", "proteins", "fats", "carbohydrates", "description", "img")
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                "name", "menu", "kind", "cost", "proteins", "fats", "carbohydrates", "description", "img"
            )}
         ),
    )
    search_fields = ("name", "kind__name", "description")
    ordering = ("id", "name", "kind", "cost", "cost_aggregated", "proteins", "fats", "carbohydrates", "description")


class CustomOrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ("id", "user", "cost", "address", "type", "status", "created", "comment")
    list_filter = ("status", "type",)
    fieldsets = (
        (None, {
            'fields': ("toppings", "status", "type",)
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                "toppings", "status", "type",
            )}
         ),
    )
    search_fields = ("user__name", "user__phone", "address__address", "comment")
    ordering = ("id", "user", "cost", "address", "type", "status", "created", "comment")
    inlines = [OrderPositionInline]


admin.site.register(Menu, CustomMenuAdmin)
admin.site.register(DishKind, CustomDishKindAdmin)
admin.site.register(ToppingKind, CustomToppingKindAdmin)
admin.site.register(Topping, CustomToppingAdmin)
admin.site.register(Dish, CustomDishAdmin)
admin.site.register(Order, CustomOrderAdmin)
