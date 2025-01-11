from django.contrib import admin
from django.contrib.admin import ModelAdmin

from books.models import Book, BookRating, Category, Wishlist


@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = (
        "name",
        "image",
        "description",
        "author",
        "slug",
        "book_audio",
        "category",
        "created_at",
        "review",
        "book_file",
    )


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = "name", "slug"


@admin.register(BookRating)
class BookRatingAdmin(ModelAdmin):
    list_display = "rating", "book", "user"


@admin.register(Wishlist)
class WishListAdmin(ModelAdmin):
    list_display = "book", "user"
