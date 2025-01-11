from django.db.models import TextChoices


class UserRoleChoices(TextChoices):
    ADMIN = "admin", "ADMIN"
    USER = "user", "USER"
    PUBLISHER = "publisher", "PUBLISHER"


class NotificationTypeChoices(TextChoices):
    SUBSCRIPTIONS = "subscriptions", "SUBSCRIPTIONS"
    NEW_BOOK = "new_book", "NEW_BOOK"
