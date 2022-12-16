from django.contrib import admin

from customer.models import Customer, Order, SecretWord, BalanceReplenishment, BalanceWriteOff


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "balance", "admin_permission")
    list_display_links = ("name", )
    empty_value_display = "-empty-"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "id", "state", "created_date", "updated_date")
    list_display_links = ("id", )
    empty_value_display = "-empty-"


@admin.register(SecretWord)
class SecretWordAdmin(admin.ModelAdmin):
    list_display = ("word", "created_date")
    list_display_links = ("word", )
    empty_value_display = "-empty-"


@admin.register(BalanceReplenishment)
class BalanceReplenishmentAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "from_customer_name", "count", "date")
    list_display_links = ("id", )
    empty_value_display = "-empty-"


@admin.register(BalanceWriteOff)
class BalanceWriteOffAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "from_customer_name", "count", "date")
    list_display_links = ("id", )
    empty_value_display = "-empty-"
