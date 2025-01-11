from django.contrib.auth.models import AbstractUser
from django.db.models import (CASCADE, DateTimeField, ForeignKey, ImageField,
                              ManyToManyField, Model, OneToOneField)
from django.db.models.fields import CharField, DateField, EmailField, TextField
from phonenumber_field.modelfields import PhoneNumberField

from users.choices import NotificationTypeChoices, UserRoleChoices
from users.managers import UserManager


class User(AbstractUser):
    username = CharField(max_length=255, unique=True, null=True, blank=True)
    role = CharField(
        max_length=20, choices=UserRoleChoices, default=UserRoleChoices.USER, null=False
    )
    birth_date = DateField(null=True, blank=True)
    email = EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    categories = ManyToManyField("books.Category", related_name="users")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    objects = UserManager()


class Profile(Model):
    fullname = CharField(max_length=255, null=True, blank=True)
    phone_number = PhoneNumberField(region="UZ", unique=True)
    image = ImageField(upload_to="profiles/")
    user = OneToOneField("users.User", CASCADE, related_name="profile")

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


class Notifications(Model):
    message = TextField()
    user = ForeignKey("users.User", CASCADE, related_name="notifications")
    type = CharField(max_length=20, choices=NotificationTypeChoices)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.email}: {self.message[:20]}"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
