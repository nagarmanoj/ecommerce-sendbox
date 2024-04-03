from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe
# from authentication.models import User
from django.contrib.auth.models import User


class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    street = models.CharField(max_length=100,null=True)
    landmark = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=50,null=True)
    state = models.CharField(max_length=50,null=True)
    country = models.CharField(max_length=50,null=True)
    zip_code = models.IntegerField(null=True)
    phone = models.CharField(max_length=50,null=True)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.street