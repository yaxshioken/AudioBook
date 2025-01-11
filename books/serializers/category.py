from rest_framework.fields import ListField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer

from books.models import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'
        read_only_fields=('id','slug')


class ChoiceCategorySerializer(Serializer):
    ids = ListField(
        child=IntegerField(),
        allow_empty=False,
        help_text="Kategoriya IDlari ro'yxatini yuboring"
    )