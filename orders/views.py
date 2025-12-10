import json
import hmac
import hashlib

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Order
from .serializers import OrderSerializer

# Import your utils
from .utils import (
    create_paystack_reference,
    initialize_paystack_payment,
    verify_paystack_transaction,
    calculate_order_total
)


class CreateOrderView(APIView):
    """
    Create a new order and assign a Paystack reference.
    """
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()

            # Assign unique Paystack reference
            order.reference = create_paystack_reference()
            order.save()

            return Response({
                "message": "Order created successfully",
                "order_id": order.id,
                "order_reference": order.reference,
                "order": OrderSerializer(order).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderStatusView(RetrieveAPIView):
    """
    Retrieve order status for frontend display.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = "id"
    permission_classes = [AllowAny]


class InitializePaymentView(APIView):
    """
    Initialize a Paystack payment for a given order.
    """
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        if order.payment_status == "paid":
            return Response({"message": "Order already paid"}, status=400)

        total_amount = calculate_order_total(order)  # utils function

        response = initialize_paystack_payment(
            amount=total_amount,
            email=order.email,
            reference=order.reference
        )

        if not response.get("status"):
            return Response({"error": "Failed to initialize payment"}, status=400)

        return Response({
            "reference": order.reference,
            "payment_url": response["data"]["authorization_url"]
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class PaystackWebhookView(APIView):
    """
    Handles Paystack webhook to update order status after payment.
    """
    def post(self, request):
        paystack_signature = request.headers.get("x-paystack-signature")

        # Validate signature
        computed_signature = hmac.new(
            settings.PAYSTACK_SECRET_KEY.encode('utf-8'),
            request.body,
            hashlib.sha512
        ).hexdigest()

        if computed_signature != paystack_signature:
            return Response({"error": "Invalid signature"}, status=400)

        event = json.loads(request.body)
        event_type = event.get("event")

        if event_type == "charge.success":
            reference = event["data"]["reference"]

            try:
                order = Order.objects.get(reference=reference)
            except Order.DoesNotExist:
                return Response({"error": "Order not found"}, status=404)

            # Verify transaction via Paystack for extra safety
            verify = verify_paystack_transaction(reference)
            if not verify.get("status"):
                return Response({"error": "Verification failed"}, status=400)

            # Update order status
            order.payment_status = "paid"
            order.order_status = "processing"
            order.save()

            return Response({"message": "Payment verified"}, status=200)

        return Response({"message": "Event ignored"}, status=200)




# Create your views here.
