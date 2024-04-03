from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from authentication.decorators import allowed_users
from store.models import Product,Brand,Category,ProductInventory,ProductType,ProductAttribute,ProductMedia,Stock
from django.http import JsonResponse
from django.views.generic.base import View
from store.models.media import Media
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.core.serializers import serialize
from django.contrib import messages
from django.utils.decorators import method_decorator
import urllib.request
import os
import random
# import pandas as pd
import string 
from django.conf import settings


######################################################################Category############################################################################
@login_required(login_url='authentication:sign-in')
@allowed_users(allowed_roles=['admin','seller','manager'])
def category_view(request):
    categories = Category.objects.all()
    context = {
        "categories":categories
    }
    return render(request,'store/category/category-list.html',context)

@csrf_exempt
def add_category_view(request):
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        fs = FileSystemStorage()
        title = request.POST["title"]
        thumbnail = request.FILES["image"]        
        filePath = fs.save(f'category/{thumbnail.name}',thumbnail)
        data = Category(
           title=title,
           thumbnail=filePath 
        )
        data.save()
        return JsonResponse({'susscess':True})
    context = {

    }
    return render(request,'store/category/add-category.html',context)

@csrf_exempt
def edit_category_view(request):
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        fs = FileSystemStorage()
        title = request.POST["title"]
        thumbnail = request.FILES["image"]        
        filePath = fs.save(f'category/{thumbnail.name}',thumbnail)
        data = Category(
           title=title,
           thumbnail=filePath 
        )
        data.save()
        return JsonResponse({'susscess':True})
    context = {

    }
    return render(request,'store/category/edit-category.html',context)

def delete_category_view(request):
    pass