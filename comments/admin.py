from django.contrib import admin
from django.contrib.admin import ModelAdmin

from comments.models import Comment, CommentRating


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = "comment", "user", "book"


@admin.register(CommentRating)
class CommentRatingAdmin(ModelAdmin):
    list_display = "user", "comment", "rating"
