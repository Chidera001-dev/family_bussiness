from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'full_name',
            'email',
            'phone_number',
            'address',
            'product',
            'quantity',
            'payment_status',
            'order_status',
            'payment_reference',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'payment_status', 'order_status', 'created_at', 'updated_at']
