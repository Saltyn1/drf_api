import django_filters.rest_framework.backends
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters import rest_framework as filters

from .filters import ProductFilter
from .models import Product, Review

# 1. Список товаров, доступен всем пользователям
from .serializers import ProductListSerializer, ProductDetailsSerializer, ReviewSerializer


# @api_view(['GET'])
# def products_list(request):
#     queryset = Product.objects.all()
#     filtered_qs = ProductFilter(request.GET, queryset=queryset)
#     serializer = ProductListSerializer(filtered_qs.qs, many=True)
#     serializer_queryset = serializer.data
#     return Response(data=serializer_queryset, status=status.HTTP_200_OK)

# class ProductsListView(APIView):
#     def get(self, request):
#         queryset = Product.objects.all()
#         filtered_qs = ProductFilter(request.GET, queryset=queryset)
#         serializer = ProductListSerializer(filtered_qs.qs, many=True)
#         serializer_queryset = serializer.data
#         return Response(data=serializer_queryset, status=status.HTTP_200_OK)

class ProductsListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ProductFilter

# 2. Детали товаров, доступны всем
class ProductDetailsView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer


class CreateProductView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer
    permission_classes = [IsAdminUser]


class UpdateProductView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer
    permission_classes = [IsAdminUser]

# 3. Создание товаров, редактирование, удаление,  доступно только админам
class DeleteProductView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer
    permission_classes = [IsAdminUser]


# 4. Создание отзывов, доступно только залогиненным пользователям
class CreateReview(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}




# 5. Просмотр отзывово(внутри деталей продукта) доступен всем
# 6. Редактирование и удаление отзыва может делать только автор
# 7. Заказы может создать любой залогиненный пользователь
# 8. Список заказов: пользователь видит только свои заказы, админы видят все заказы
# 9. Редактировать заказы может только админ
#
# '''

