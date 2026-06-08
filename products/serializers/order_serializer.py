from django.core.exceptions import ObjectDoesNotExist
from products.models.product_model import Product
from products.models.order_model import Order
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'product', 'customer', 'quantity', 'created_at', 'total_price', 'phone_number', 'is_paid']

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity

    def validate_quantity(self, value):
        try:
            product_id = self.initial_data['product']
            product = Product.objects.get(id=product_id)

            if value > product.stock:
                raise serializers.ValidationError('Not enough items in stock!')
            if value < 0:
                raise serializers.ValidationError('Quantity must be at least 1!')
            return value

        except ObjectDoesNotExist:
            raise serializers.ValidationError('Product does not exist!')

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        product = order.product
        product.stock -= order.quantity
        product.save()
        return order
