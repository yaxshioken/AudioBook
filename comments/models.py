from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (CASCADE, SET_NULL, DateTimeField, ForeignKey,
                              IntegerField, Model, TextField)


class Comment(Model):
    comment = TextField()
    created_at = DateTimeField(auto_now_add=True)
    user = ForeignKey(
        "users.User", SET_NULL, related_name="comments", null=True, blank=True
    )
    book = ForeignKey("books.Book", CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.comment[:30]}..."

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class CommentRating(Model):
    user = ForeignKey(
        "users.User", SET_NULL, related_name="rating", null=True, blank=True
    )
    comment = ForeignKey("comments.Comment", CASCADE, related_name="rating")
    rating = IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    unique_together = ("user", "comment")

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
        unique_together = ("user", "comment")

    def __str__(self):
        return f"User: {self.user} | Comment: {self.comment.id} | Rating: {self.rating}"
