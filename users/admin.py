from django.contrib import admin
from django.contrib.admin import ModelAdmin

from users.models import Notifications, Profile, User


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = "email", "role", "birth_date"
    list_editable = ("role",)


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = "fullname", "phone_number", "image", "user"


@admin.register(Notifications)
class NotificationAdmin(ModelAdmin):
    list_display = "message", "user", "created_at", "type"
