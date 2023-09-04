from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from apps.categories.models import Service_category
from apps.service.models import ProductImage, Characteristic, Product, AdditionalInformation, Promotion, PromotionType
from apps.service.serializers import (ProductCreateSerializer, CharacteristicListSerializer, CategoryListSerializer,
                                      ProductUpdateSerializer, ProductListSerializer, PromotionTypeListSerializer,
                                      PromotionCreateSerializer, PromotionUpdateSerializer)
from apps.service.pagination import ProductPagination


class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        characteristic = Characteristic.objects.filter(category__id=pk)
        category = Service_category.objects.filter(parent__isnull=False)
        print(category)

        characteristic_serializer = CharacteristicListSerializer(characteristic, many=True)
        category_serializer = CategoryListSerializer(category, many=True)

        all_data = {
            'category': category_serializer.data,
            'characteristic': characteristic_serializer.data
        }

        return Response(all_data)

    def post(self, request, pk, format=None):
        serializer = ProductCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductUpdateView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductUpdateSerializer


class MyProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user.id).order_by('-id')


class PromotionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        products = Product.objects.filter(user=self.request.user.id).order_by('-id')
        products_serializer = ProductListSerializer(products, many=True)

        promotion_type = PromotionType.objects.all()
        promotion_type_serializer = PromotionTypeListSerializer(promotion_type, many=True)

        all_data = {
            'products': products_serializer.data,
            'promotion_type': promotion_type_serializer.data
        }

        return Response(all_data)

    def post(self, request, format=None):
        serializer = PromotionCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PromotionUpdateView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Promotion.objects.all()
    serializer_class = PromotionUpdateSerializer


