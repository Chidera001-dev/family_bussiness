from django.urls import path
from .views import (
    CreateOrderView,
    InitializePaymentView,
    PaystackWebhookView,
    OrderStatusView
)

urlpatterns = [
    path("create/", CreateOrderView.as_view(), name="create-order"),
    path("pay/<str:order_id>/", InitializePaymentView.as_view(), name="initiate-payment"),
    path("status/<str:id>/", OrderStatusView.as_view(), name="order-status"),
    path("webhook/paystack/", PaystackWebhookView.as_view(), name="paystack-webhook"),
]
