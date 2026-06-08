from django.db import models
from django.core.validators import RegexValidator
from .product_model import Product
from custom_auth.types import User

phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message='Phone number must be entered in the format: +998xxxxxxxxx'
)


class Order(models.Model):
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELED = 'Canceled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(validators=[phone_regex], max_length=13)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    is_paid = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_status(self, new_status):
        if new_status not in dict(self.STATUS_CHOICES):
            self.status = new_status
            self.save()

    def is_transition_allowed(self, new_status):
        allowed_transitions = {
            self.PENDING: [self.PROCESSING, self.CANCELED],
            self.PROCESSING: [self.SHIPPED, self.CANCELED],
            self.SHIPPED: [self.DELIVERED, self.CANCELED],
        }
        return new_status in allowed_transitions.get(self.status, [])

    def __str__(self):
        return f"Order({self.product.name} by {self.customer.username})"