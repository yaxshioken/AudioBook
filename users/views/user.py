import json

from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from redis import Redis
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainSlidingView

from users.models import User
from users.serializers.user import RegisterSerializer, CheckCodeSerializer, LoginSerializer
from users.tasks import send_email


class RegisterAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    my_tags = ["register", ]
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        birth_date = request.data.get('birth_date')
        query = User.objects.filter(email=email)
        if query.exists():
            raise ValidationError({"error": "Bunday email mavjud!"})

        r = Redis(decode_responses=True)
        data = {"email": email, "password": password, "birth_date": birth_date}
        r.set(email, json.dumps(data))
        send_email.delay(email)
        return Response(data={"success": "Emailingizni Tekshiring!!!"})


class CheckCodeAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = CheckCodeSerializer
    my_tags = ["checkcode", ]
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(request_body=CheckCodeSerializer)
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        r = Redis(decode_responses=True)
        email_code = r.get(f'code:{email}')

        if email_code is None or code != email_code:
            raise ValidationError({"error": "Kodning   muddati o'tgan yoki Email xato!!!"})
        data = r.get(email)
        if data is None:
            raise ValidationError({"error": "Bunday email uchun ro'yxatdan o'tish ma'lumotlari mavjud emas!"})
        data = json.loads(data)

        password = data['password']
        password = make_password(password)
        birth_date = data['birth_date']
        user = User.objects.create(email=email, password=password, birth_date=birth_date)
        return Response({"success": "True"}, status=200)


class LoginView(TokenObtainSlidingView):
    serializer_class = LoginSerializer
    my_tags = ["login", ]
    permission_classes = [AllowAny, ]
