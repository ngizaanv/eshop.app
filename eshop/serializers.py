from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):


    class Meta:
        model = Category
        fields = ['name']

class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discount
        fields = ['discount']

class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['email']


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    supplier = UserSerializer()
    discount = DiscountSerializer()

    class Meta:
        model = Product
        fields = ['title', 'description', 'created', 'pictures', 'price', 'discount', 'supplier', 'category']

    def create(self, validated_data):
        supplier_data = validated_data.pop('supplier')
        supplier = User.objects.create(**supplier_data)
        product = Product.objects.create(**validated_data, supplier=supplier)
        discount_data = validated_data.pop('discount')
        category = Discount.objects.create(**discount_data)
        product = Product.objects.create(**validated_data, discount=discount)
        category_data = validated_data.pop('category')
        category = Category.objects.create(**category_data)
        product = Product.objects.create(**validated_data, category=category)

        return product

class CommentSerializer(serializers.ModelSerializer):

    author = UserSerializer()

    class Meta:
        model = Comment
        fields = ['author', 'rate', 'content', 'created', 'replies']

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author = User.objects.create(**author_data)
        comment = Comment.objects.create(**validated_data, author=author)

        return comment

class CartSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Cart
        fields = ['user', 'total_price', 'in_order']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        cart = Cart.objects.create(**validated_data, user=user)

        return cart

class CartProductSerializer(serializers.ModelSerializer):

    cart = CartSerializer()
    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = ['quantity', 'product', 'price', 'cart']

    def create(self, validated_data):
        product_data = validated_data.pop('product')
        product = Product.objects.create(**product_data)
        cartproduct = CartProduct.objects.create(**validated_data, product=product)
        cart_data = validated_data.pop('cart')
        cart = Cart.objects.create(**cart_data)
        cartproduct = CartProduct.objects.create(**validated_data, cart=cart)

        return cartproduct




