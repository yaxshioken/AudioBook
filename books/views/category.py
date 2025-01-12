from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Category
from books.serializers.category import (CategorySerializer,
                                        ChoiceCategorySerializer)


@extend_schema(
    request=CategorySerializer, responses={201: CategorySerializer}, tags=["books"]
)
class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    my_tags = ["categories"]


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    my_tags = ["categories"]


class ChoiceCategoryAPIView(APIView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = ChoiceCategorySerializer
    my_tags = ["categories"]

    def post(self, request):
        serializer = ChoiceCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ids = serializer.validated_data.get("ids", [])

        user = request.user
        categories = Category.objects.filter(id__in=ids)
        if len(ids) != categories.count():
            missing_ids = set(ids) - set(categories.values_list("id", flat=True))
            return Response(
                {
                    "error": f"Kiritilgan IDlar topilmadi: {', '.join(map(str, missing_ids))}"
                },
                status=404,
            )

        if not categories.exists():
            return Response(
                {"error": "Kiritilgan ID bo'yicha kategoriya topilmadi"}, status=404
            )
        user.categories.set(categories)
        user.save()
        return Response({"message": "Kategoriyalar muvaffaqiyatli saqlandi!"}, 200)
