from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from store.models.category import Category
from store.models.product import Product



class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return self.product.title 