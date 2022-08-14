from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *


class ProductsViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class CommentsViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product_id']

class CartProductsViewSet(ModelViewSet):
    serializer_class = CartProductSerializer
    queryset = CartProduct.objects.all()

class CartsViewSet(ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.filter(in_order=False)











