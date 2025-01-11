from django.urls import path

from books.views.category import CategoryCreateAPIView, CategoryListAPIView, ChoiceCategoryAPIView

urlpatterns=[
    path("category-create/",CategoryCreateAPIView.as_view(),name='create-category'),
    path("category-list/",CategoryListAPIView.as_view(),name='create-category'),
    path("category-choice/",ChoiceCategoryAPIView.as_view(),name='create-choice'),

]