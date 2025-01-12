from django.contrib import admin
from django.contrib.admin import ModelAdmin

from payment.models import CreditCard, Orders, Subscribe


@admin.register(Orders)
class OrderAdmin(ModelAdmin):
    list_display = (
        "card_number",
        "created_at",
        "expired_date",
        "cost_amount",
        "user",
        "subscribe",
    )


@admin.register(Subscribe)
class SubscribeAdmin(ModelAdmin):
    list_display = "price", "description", "type"


@admin.register(CreditCard)
class CreditCardAdmin(ModelAdmin):
    list_display = "user", "card_number", "expired_date", "card_holder_name"
