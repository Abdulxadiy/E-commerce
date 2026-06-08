from products.models import FlashSale, Product, ProductViewHistory
from rest_framework import serializers, generics
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class FlashSaleListCreateView(generics.ListCreateAPIView):
    queryset = FlashSale.objects.all()

    class FlashSaleSerializer(serializers.ModelSerializer):
        class Meta:
            model = FlashSale
            fields = '__all__'

    serializer_class = FlashSaleSerializer


@api_view(['GET'])
def check_flash_sale(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': "Product not found!"}, status=status.HTTP_404_NOT_FOUND)

    user_viewed = ProductViewHistory.objects.filter(user=request.user, product=product).exists()

    upcoming_flash_sale = FlashSale.objects.filter(product=product, start_time__lte=timezone.now() + timedelta(hours=24)).first()


    if user_viewed and upcoming_flash_sale:
        discount = upcoming_flash_sale.discount_percentage
        start_time = upcoming_flash_sale.start_time
        end_time = upcoming_flash_sale.end_time

        return Response({
            'message': f"Flash sale coming up! \nGet {discount}% off from {start_time} to {end_time}."
        })
    else:
        return Response({'message': "No flash sale available for this product."})

