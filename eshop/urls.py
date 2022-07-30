from django.urls import path

from eshop import views

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='get_post_product'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='get_delete_product'),
]