from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import os

class Media(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length=255, blank=True)
    file = models.URLField(max_length = 255,null=True,blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension