from django.urls import path

from users.views.user import (ChangePasswordAPIView, CheckCodeAPIView,
                              ConfirmEmailAPIView, ForgetPassAPIView,
                              LoginView, RegisterAPIView)

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="user-register"),
    path(
        "change_password/<str:url>/",
        ChangePasswordAPIView.as_view(),
        name="user-change-password",
    ),
    path("login/", LoginView.as_view(), name="user-login"),
    path("forgetpassword/", ForgetPassAPIView.as_view(), name="user-forget-password"),
    path(
        "confirm_email/<str:url>/",
        ConfirmEmailAPIView.as_view(),
        name="user-confirm-email",
    ),
    path("check_email_code/", CheckCodeAPIView.as_view(), name="user-check-email-code"),
]
