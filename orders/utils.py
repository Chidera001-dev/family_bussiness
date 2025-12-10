from django.conf import settings
from paystackapi.paystack import Paystack

# Initialize Paystack SDK
paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)

# Supported currencies and channels
SUPPORTED_CURRENCIES = ["NGN", "GHS", "USD", "ZAR"] 
SUPPORTED_CHANNELS = [
    "card",
    "bank",
    "ussd",
    "qr",
    "mobile_money",
    "bank_transfer",
    "eft",      # For South Africa
    "paypal",   # If enabled on your Paystack dashboard
]


def initialize_paystack_payment(email: str, amount: float, reference: str, currency: str = "NGN") -> dict:
    """
    Initialize a Paystack transaction.
    - NGN → converted to kobo (amount * 100)
    - Other currencies stay as-is
    - Uses all supported payment channels
    """
    currency = currency.upper()
    if currency not in SUPPORTED_CURRENCIES:
        raise ValueError(f"Unsupported currency: {currency}")

    # Convert NGN to kobo
    if currency == "NGN":
        paystack_amount = int(amount * 100)
    else:
        paystack_amount = float(amount)

    response = paystack.transaction.initialize(
        email=email,
        amount=paystack_amount,
        reference=reference,
        currency=currency,
        channels=SUPPORTED_CHANNELS
    )
    return response


def verify_paystack_transaction(reference: str) -> dict:
    """
    Verify a Paystack transaction by its reference.
    """
    return paystack.transaction.verify(reference)


def create_paystack_reference() -> str:
    """
    Generate a unique transaction reference for Paystack.
    """
    import shortuuid
    return shortuuid.uuid()


def calculate_order_total(order) -> float:
    """
    Calculate total amount for an order (product price x quantity).
    """
    return float(order.product.price) * int(order.quantity)

