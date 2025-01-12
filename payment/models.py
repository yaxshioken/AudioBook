from creditcards.models import CardNumberField
from django.db.models import CASCADE, SET_NULL, ForeignKey, Model
from django.db.models.fields import (CharField, DateTimeField, DecimalField,
                                     TextField)

from payment.choices import SubscribeChoices


class Subscribe(Model):
    price = DecimalField(max_digits=10, decimal_places=2)
    description = TextField()
    type = CharField(max_length=255, choices=SubscribeChoices)

    class Meta:
        verbose_name = "Subscribe"
        verbose_name_plural = "Subscribes"

    def __str__(self):
        return f"{self.type} ({self.price} $)"


class Orders(Model):
    user = ForeignKey(
        "users.User", SET_NULL, related_name="user_orders", null=True, blank=True
    )
    subscribe = ForeignKey(
        "payment.Subscribe",
        SET_NULL,
        related_name="subscribe_orders",
        null=True,
        blank=True,
    )
    card_number = ForeignKey(
        "payment.CreditCard", SET_NULL, related_name="orders", null=True, blank=True
    )
    created_at = DateTimeField(auto_now_add=True)
    expired_date = DateTimeField()
    cost_amount = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{self.id} - {self.user} - {self.cost_amount} $"


class CreditCard(Model):
    user = ForeignKey("users.User", CASCADE, related_name="credit_cards")
    card_number = CardNumberField()
    expired_date = DateTimeField()
    card_holder_name = CharField(max_length=255)

    def __str__(self):
        return f"{self.card_holder_name} ({self.card_number[-4:]})"
