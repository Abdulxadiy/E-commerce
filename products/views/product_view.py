from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from products.serializers.misc import ProductSerializer
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from products.models.product_model import Product
from products.filters import ProductFilter
from django.db import models


class CustomPagination(PageNumberPagination):
    page_size = 5


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.annotate(avg_rating=models.Avg('reviews__rating'))
    serializer_class = ProductSerializer

    permission_classes = [IsAuthenticated]

    pagination_class = CustomPagination

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProductFilter
    search_filter = ['name', 'description']

    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category', None)

        if category:
            self.queryset = self.queryset.filter(category=category)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_products  = Product.objects.filter(category=instance.category).exclude(id=instance.id)[:5]
        related_serializer = self.get_serializer(related_products, many=True)
        return Response({
            'product': serializer.data,
            'related_products': related_serializer.data
        })

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        top_products = Product.objects.annotate(avg_rating=models.Avg('reviews__rating')).order_by('-avg_rating')[:3]
        serializer = ProductSerializer(top_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def average_rating(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()

        if reviews.count() == 0:
            return Response({"average_rating": "No reviews yet!"})

        avg_rating = sum([review.rating for review in reviews]) / reviews.count()

        return Response({"average_rating": avg_rating})