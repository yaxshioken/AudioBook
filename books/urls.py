from django.urls import path

from books.views.books import BookCreateAPIView, RecommendedBooksAPIView, NewReleasesAPIView, TrendingNowAPIView, \
    BookRetrieveAPIView
from books.views.category import (CategoryCreateAPIView, CategoryListAPIView,
                                  ChoiceCategoryAPIView)

urlpatterns = [
    path("category-create/", CategoryCreateAPIView.as_view(), name="create-category"),
    path("category-list/", CategoryListAPIView.as_view(), name="create-category"),
    path("category-choice/", ChoiceCategoryAPIView.as_view(), name="choice-category"),
    # Book
    path("book-create/", BookCreateAPIView.as_view(), name="book-create"),
    path("book-retrieve/<int:id>/", BookRetrieveAPIView.as_view(), name="book-retrieve"),
    path("recommended_books/", RecommendedBooksAPIView.as_view(), name='recommended-books'),
    path("new_releases/", NewReleasesAPIView.as_view(), name='new-releases'),
    path("trending_now/", TrendingNowAPIView.as_view(), name='trending-now')
]
