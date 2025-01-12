from rest_framework.serializers import ModelSerializer

from books.models import Book


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ("slug", "created_at", "review")
