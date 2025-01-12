from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from books.models import Book
from books.serializers.book import BookSerializer


class GlobalSearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = kwargs.get('search', '')

        if not query:
            return Response({"error": "Qidiruv so'rovini kiriting!"}, status=400)
        books = Book.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)|
            Q(author__icontains=query) | Q(slug__icontains=query)|
            Q(image__icontains=query) | Q(book_audio__icontains=query)
        )
        results = {
            "books": [{"name": b.name, "description": b.description, "author": b.author,"slug":b.slug,"image":b.image,
                       "book_audio":b.book_audio} for b in books],

        }
        serializer=BookSerializer(results)
        return Response(serializer.data,200)

        return Response(results)
