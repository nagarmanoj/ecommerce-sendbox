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


######################################################################## Brand ######################################################################################################
@login_required(login_url='authentication:sign-in')
@allowed_users(allowed_roles=['admin','seller','manager'])
def brand_view(request):
    brands = Brand.objects.all()
    context = {
        "brands":brands
    }
    return render(request,'store/brand/brand-list.html',context)

def add_brand_view(request):
    if request.method == 'POST':
        title = request.POST['title']
        # image = request.FILES['image']
        description = request.POST['description']
        
        data = Brand(
            title=title,
            description=description,            
            # thumbnail=image
        )
        print(data)
        data.save()

        return JsonResponse({'success': True})
    
    
    context = {
       
    }
    return render(request,'store/brand/add-brand.html',context)

@csrf_exempt
def edit_brand_view(request,bid):    
    brand = Brand.objects.get(bid=bid)
    print(brand)
    if request.method == 'POST':        
        print(request.POST)
        print(request.FILES)        
        # image = request.FILES['image']
        description = request.POST["description"]
        data = Brand.objects.filter(bid=bid).update_or_create(            
            description=description,
        )
        print(data)
        

        return JsonResponse({'success': True})
    
    
    context = {
       "brand":brand
    }
    return render(request,'store/brand/edit-brand.html',context)

def delete_brand_view(request):
    try:
        if request.GET.get('bid'):
            brand = Brand.objects.filter(bid=request.GET.get('bid')).delete()
            messages.success(request,f"Item  delete successfully !")          
        
    except Exception as e:
        print(f"Something want wrong {e}")

    brands = Brand.objects.all()
    context={
        "brands":brands
    }
    return render(request,"store/brand/brand-list.html",context)