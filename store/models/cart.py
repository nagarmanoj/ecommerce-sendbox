from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from store.models import Product
from django.core.validators import MinValueValidator
from decimal import Decimal


STATUS_CHOICE = (
    ("process","Processing"),
    ("shipped","Shipped"),
    ("delived","Delivered"),
)


################################################################### Cart, Cart Items ########################################################


class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    products = models.ManyToManyField(Product,through='Cartitem')

    def __str__(self):
        return f"Cart for {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=1)
    

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

###########################################################################Order,OrderItems #########################################
class CartOrder(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices=STATUS_CHOICE,max_length=30,default="processing")


    class Meta:
        verbose_name_plural = "Cart Orders"

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])


    class Meta:
        verbose_name_plural = "Cart Orders Items"