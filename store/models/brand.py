from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from autoslug import AutoSlugField

class Brand(models.Model):
    bid = ShortUUIDField(unique=True, length=10,max_length=20,alphabet="abcdefgh12345")    
    title = models.CharField(max_length=255,unique=True)
    slug_url = AutoSlugField(populate_from='title',editable=True, always_update=True)
    thumbnail = models.URLField(null=True)   
    description= models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Brands"
    

    def __str__(self):
        return self.title