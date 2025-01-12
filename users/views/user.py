import json

from django.contrib.auth.hashers import make_password
from drf_spectacular.utils import extend_schema
from redis import Redis
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainSlidingView

from users.models import User
from users.serializers.user import (ChangePasswordSerializer,
                                    CheckCodeSerializer,
                                    ForgotPasswordSerializer, LoginSerializer,
                                    RegisterSerializer)
from users.tasks import change_password, confirm_email, send_email_code


class RedisClient:
    _client = None

    @staticmethod
    def get_client():
        if RedisClient._client is None:
            RedisClient._client = Redis(
                host="localhost", port=6379, db=0, decode_responses=True
            )
        return RedisClient._client


def raise_custom_error(error_code, message):
    raise ValidationError({"error_code": error_code, "message": message})


def hash_password(password):
    return make_password(password)


class RegisterAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(request=RegisterSerializer, tags=["auth"])
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        birth_date = request.data.get("birth_date")

        if User.objects.filter(email=email).exists():
            raise_custom_error("ERROR", "Foydalanuvchi ro'yxatdan o'tgan!!!")

        redis_client = RedisClient.get_client()
        data = {"email": email, "password": password, "birth_date": birth_date}
        send_email_code.delay(email)
        redis_client.setex(email, 3600, json.dumps(data))
        return Response(data={"success": "Emailingizni tekshiring kod yuborildi !!!"})


class CheckCodeAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = CheckCodeSerializer
    permission_classes = [AllowAny]

    @extend_schema(request=CheckCodeSerializer, tags=["auth"])
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        redis_client = RedisClient.get_client()
        email_code = redis_client.get(f"code:{email}")

        if email_code is None or code != email_code:
            raise_custom_error(
                "INVALID_CODE", "Kodning muddati o'tgan yoki email noto'g'ri!"
            )

        data = redis_client.get(email)
        if not data:
            raise_custom_error(
                "NOT_FOUND",
                "Bunday email uchun ro'yxatdan o'tish ma'lumotlari mavjud emas!",
            )

        data = json.loads(data)
        password = hash_password(data["password"])
        birth_date = data["birth_date"]
        User.objects.create(email=email, password=password, birth_date=birth_date)
        redis_client.delete(email)

        return Response(
            {"success": "Siz muvaffaqiyatli ro'yxatdan o'tdingiz!!!"}, status=200
        )


@extend_schema(tags=["auth"])
class LoginView(TokenObtainSlidingView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]


class ForgetPassAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=ForgotPasswordSerializer, tags=["auth"])
    def post(self, request):
        email = request.data.get("email")

        if not User.objects.filter(email=email).exists():
            raise_custom_error("NOT_FOUND", "Topilmadi!!!")
        confirm_email.delay(email)
        return Response(
            {"success": "Emailga xabar yuborildi, emailingizni tekshiring!"}, status=200
        )


class ConfirmEmailAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(tags=["auth"])
    def get(self, request, url):
        redis_client = RedisClient.get_client()
        url = request.path.split("/")[-2]
        stored_email = redis_client.get(url)

        if not stored_email:
            raise_custom_error("EXPIRED", "URL muddati o'tgan yoki noto'g'ri!")
        change_password.delay(stored_email)

        return Response(
            {"success": f"Email {stored_email} tasdiqlandi! Emailingizni tekshiring!"},
            status=200,
        )


class ChangePasswordAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ChangePasswordSerializer

    @extend_schema(tags=["auth"], request=ChangePasswordSerializer)
    def post(self, request, url):
        redis_client = RedisClient.get_client()
        url = request.path.split("/")[-2]
        stored_email = redis_client.get(url)

        if not stored_email:
            raise_custom_error(
                "NOT_FOUND", "Foydalanuvchi topilmadi yoki ma'lumot muddati o'tgan!"
            )

        user = User.objects.filter(email=stored_email).first()

        if not user:
            raise_custom_error("NOT_FOUND", "Foydalanuvchi topilmadi!")
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user.password = hash_password(serializer.validated_data["password"])
            user.save()
            redis_client.delete(url)
            return Response(
                {"success": "Parol muvaffaqiyatli o'zgartirildi!"}, status=200
            )
        return Response(serializer.errors, status=400)


