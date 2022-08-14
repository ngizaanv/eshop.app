from rest_framework.test import APITestCase
from django.test import TestCase

from eshop.models import *

class TestModel(APITestCase):
    def test_create_user(self):
        user=User.objects.create_user('ashdasdh@gmai.com', 'password123')
        self.assertIsInstance(user,User)
        self.assertFalse(user.is_admin)
        self.assertEqual(user.email, 'ashdasdh@gmai.com')

    def test_create_superuser(self):
        user=User.objects.create_superuser('ashdasdh@gmai.com', 'password123')
        self.assertIsInstance(user,User)
        self.assertTrue(user.is_admin)
        self.assertEqual(user.email, 'ashdasdh@gmai.com')

    def test_when_no_email(self):
        self.assertRaises(ValueError, User.objects.create_user, email='', password='password123')
        with self.assertRaisesMessage(ValueError, 'Users must have an email address'):
            User.objects.create_user('', 'password123')


class EshopModelTestStr(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(title='Destination', description='))((', price=100, category_id=1, supplier_id=1,
                               discount_id=1)
        Product.objects.create(title='test', description='))((', price=100, category_id=1, supplier_id=1,
                               discount_id=2)
        Category.objects.create(name='Language courses')

        Discount.objects.create(discount=41)
        Discount.objects.create(discount=0)

        Comment.objects.create(author_id=1, rate=4, content='its amaizing!')
        User.objects.create(email='ashdasdh@gmai.com', password=123456)
        Cart.objects.create(user_id=1, in_order=False)

        CartProduct.objects.create(quantity=2, cart_id=1, product_id=1, price=0)
        CartProduct.objects.create(quantity=2, cart_id=1, product_id=2, price=0)

    def test_cartproduct_save(self):
        cartproduct = CartProduct.objects.get(id=2)
        expected_price = cartproduct.product.price * cartproduct.quantity
        self.assertEqual(expected_price, cartproduct.price)

    def test_cartproduct_save_if_discount(self):
        cartproduct = CartProduct.objects.get(id=1)
        expected_price = (cartproduct.product.price - cartproduct.product.price*cartproduct.product.discount.discount/100) * cartproduct.quantity
        self.assertEqual(expected_price, cartproduct.price)

    def test_product_str(self):
        product = Product.objects.get(id=1)
        expected_name = product.title
        self.assertEqual(expected_name, str(product))

    def test_category_str(self):
        category = Category.objects.get(id=1)
        expected_name = category.name
        self.assertEqual(expected_name, str(category))

    def test_discount_str(self):
        discount = Discount.objects.get(id=1)
        expected_name = str(discount.discount)
        self.assertEqual(expected_name, str(discount))

    def test_comment_str(self):
        comment = Comment.objects.get(id=1)
        expected_name = comment.content
        self.assertEqual(expected_name, str(comment))

    def test_user_str(self):
        user = User.objects.get(id=1)
        expected_name = user.email
        self.assertEqual(expected_name, str(user))

    def test_cart_str(self):
        cart = Cart.objects.get(id=1)
        expected_name = cart.user.email
        self.assertEqual(expected_name, str(cart))


