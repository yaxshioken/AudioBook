from django.db.models import TextChoices


class SubscribeChoices(TextChoices):
    ONE_MONTH = "1 oylik", "ONE_MONTH"
    THREE_MONTHS = "3 oylik", "THREE_MONTHS"
    SIX_MONTHS = "6 oylik", "SIX_MONTHS"
    ONE_YEAR = "1 yillik", "ONE_YEAR"
