from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from books.models import Book
from books.serializers.book import BookSerializer


@extend_schema(request=BookSerializer, responses={201: BookSerializer}, tags=["books"])
class BookCreateAPIView(CreateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = (AllowAny,)
    my_tags = ["books"]
