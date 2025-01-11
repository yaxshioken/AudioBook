from django.urls import path

from users.views.user import RegisterAPIView, CheckCodeAPIView, LoginView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path('check/',CheckCodeAPIView.as_view(),name='check'),
    path('login/',LoginView.as_view(),name='login')
]
