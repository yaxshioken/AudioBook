from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book
from books.serializers.book import BookSerializer


@extend_schema(request=BookSerializer, responses={201: BookSerializer}, tags=["books"])
class BookCreateAPIView(CreateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = (AllowAny,)
    my_tags = ["books"]


class BookRetrieveAPIView(RetrieveAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    lookup_field = 'id'


class RecommendedBooksAPIView(APIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request):

        categories = request.user.categories.all()
        if categories.exists():
            books = Book.objects.filter(category__id__in=categories)
        else:
            books = Book.objects.all()

        serializer = self.serializer_class(books, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class NewReleasesAPIView(ListAPIView):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer


class TrendingNowAPIView(ListAPIView):
    queryset = Book.objects.all().order_by('-rating')
    serializer_class = BookSerializer
