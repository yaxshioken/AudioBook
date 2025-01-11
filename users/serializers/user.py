from redis import Redis
from rest_framework.fields import CharField, EmailField
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "birth_date")


class CheckCodeSerializer(Serializer):
    email = EmailField()
    code = CharField()


class LoginSerializer(TokenObtainPairSerializer):
    email=EmailField()
    password=CharField()