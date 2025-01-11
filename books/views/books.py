from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from books.models import Book
from books.serializers.book import BookSerializer


class BookCreateAPIView(CreateAPIView):
    serializer_class =BookSerializer
    queryset = Book.objects.all()
    permission_classes = (AllowAny,)
    my_tags=['books']