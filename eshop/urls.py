from django.urls import path, include
from rest_framework import routers
from .views import ProductsViewSet, CommentsViewSet, CartsViewSet, CartProductsViewSet

router = routers.SimpleRouter()
router.register(r'products', ProductsViewSet)
router.register(r'comments', CommentsViewSet)
router.register(r'carts', CartsViewSet)
router.register(r'cartproducts', CartProductsViewSet)
urlpatterns = router.urls

