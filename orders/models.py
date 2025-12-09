import shortuuid
from django.db import models
from products.models import Product 


class Order(models.Model):
    # Unique ID for each order
    id = models.CharField(
        primary_key=True,
        max_length=22,
        default=shortuuid.uuid,
        editable=False,
        unique=True
    )

    # Customer details
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()

    # Product purchased (you have only one product)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    # Order and payment status
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )

    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
    ]
    order_status = models.CharField(
        max_length=10,
        choices=ORDER_STATUS_CHOICES,
        default='pending'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional: store payment reference from gateway
    payment_reference = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} - {self.full_name}"



# Create your models here.
