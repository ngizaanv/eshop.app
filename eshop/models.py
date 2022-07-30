from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.conf import settings




class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Discount(models.Model):
    discount = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return str(self.discount)

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.is_admin = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )

        user.set_password(password)
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin
    #
    # def has_perm(self, perm, obj=None):
    #     return self.is_admin
    #
    # def has_module_perms(self, app_label):
    #     return True

class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    pictures = models.ImageField(upload_to='images/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    supplier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='product', blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    product = models.ManyToManyField(Product, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    in_order = models.BooleanField(default=False)

    def total(self):
        cart_products = CartProduct.objects.filter(cart=self.pk)
        total_price = 0
        for cart_product in cart_products:
            total_price += cart_product.product.price
        return total_price

    def __str__(self):
        return str(self.total_price)


class CartProduct(models.Model):
    quantity = models.PositiveIntegerField(blank=True, default=1)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)


    def save(self, *args, **kwargs):
        if self.product.discount > 0:
            self.price = (self.product.price - self.product.price * self.product.discount / 100) * self.quantity
        else:
            self.price = self.product.price * self.quantity
        super(CartProduct, self).save(*args, **kwargs)



class Comment(models.Model):
    RATING_RANGE = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rate = models.IntegerField(choices=RATING_RANGE,)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    replies = models.ForeignKey("Comment", related_name='comment', blank=True, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='comment', blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.content




