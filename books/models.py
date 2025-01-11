from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (CASCADE, SET_NULL, CharField, DateTimeField,
                              FileField, ForeignKey, ImageField, IntegerField,
                              Model, SlugField, TextField)
from django.utils.text import slugify


# Create your models here.
class Category(Model):
    name = CharField(max_length=255, unique=True)
    slug = SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Book(Model):
    name = CharField(max_length=255, unique=True)
    image = ImageField(upload_to="book_images/")
    description = TextField()
    author = CharField(max_length=255)
    slug = SlugField(unique=True, blank=True, null=True)
    book_audio = FileField(upload_to="audios/")
    category = ForeignKey("books.Category", SET_NULL, null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    review = IntegerField(default=0     )
    book_file = FileField(upload_to="books/")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"


class Wishlist(Model):
    user = ForeignKey("users.User", CASCADE, related_name="wishlists")
    book = ForeignKey("books.Book", CASCADE, related_name="wishlists")

    def __str__(self):
        return f"User:---{self.user}---|Wishlist====    Book:{self.book}"

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"


class BookRating(Model):
    user = ForeignKey(
        "users.User", SET_NULL, related_name="ratings", null=True, blank=True
    )
    book = ForeignKey("books.Book", CASCADE, related_name="ratings")
    rating = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    unique_together = ("user", "book")

    def __str__(self):
        return f"{self.user} rated {self.book} -> {self.rating}"

    class Meta:
        verbose_name = "BookRating"
        verbose_name_plural = "BookRatings"
