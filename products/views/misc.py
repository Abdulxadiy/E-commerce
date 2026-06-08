from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from products.permissions import IsOwnerOrReadOnly
from products.models.misc import Review
from products.models.order_model import Order
from products.models.product_model import Category
from products.serializers.misc import CategorySerializer, ReviewSerializer
from products.serializers.order_serializer import OrderSerializer


class CustomPagination(PageNumberPagination):
    page_size = 5

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    pagination_class = CustomPagination

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

