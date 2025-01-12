from rest_framework.exceptions import ValidationError
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
    email = EmailField()
    password = CharField()


class ForgotPasswordSerializer(Serializer):
    email = EmailField()


class ChangePasswordSerializer(Serializer):
    password = CharField(write_only=True, style={"input_type": "password"})
    confirm_password = CharField(write_only=True, style={"input_type": "password"})

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        if password != confirm_password:
            raise ValidationError(
                (
                    {
                        "error_code": "INVALID_PASSWORD",
                        "message": "Parollar bir-biriga mos emas",
                    }
                )
            )
        return attrs
