from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_telegram_notification
from .models import Order
from django.conf import settings
import requests

@receiver(post_save, sender=Order)
def notify_admin(sender, instance, created, **kwargs):
    if created:  # Check if a new record is created
        send_telegram_notification.delay(
            order_id=instance.id,
            product_name=instance.product.name,
            quantity=instance.quantity,
            customer_username=instance.customer.username,
            phone_number=instance.phone_number
        )