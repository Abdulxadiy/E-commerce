from django_filters import rest_framework as filters
from .models.product_model import Product
from .models.misc import FlashSale

class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category']


class FlashSaleFilter(filters.FilterSet):
    min_discount = filters.NumberFilter(field_name='discount_percentage', lookup_expr='gte')
    max_discount = filters.NumberFilter(field_name='discount_percentage', lookup_expr='lte')

    start_after = filters.DateTimeFilter(field_name='start_time', lookup_expr='gte')
    end_before = filters.DateTimeFilter(field_name='end_time', lookup_expr='lte')

    class Meta:
        model = FlashSale
        fields = []
