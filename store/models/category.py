from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _

class Category(MPTTModel):
    cid = ShortUUIDField(unique=True, length=10,max_length=20,prefix="cat",alphabet="abcdefgh12345")
    name = models.CharField(max_length=100,unique=True)
    slug = AutoSlugField(unique=True,populate_from='name',editable=True, always_update=True)
    thumbnail = models.URLField(max_length=255,null=True,blank=True)    
    description= models.TextField(blank=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name
    

