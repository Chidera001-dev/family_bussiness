from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(ReadOnlyModelViewSet):
    """
    GET /products/        → list products
    GET /products/<id>/   → single product
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer




# Create your views here.
