from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication.decorators import allowed_users
from store.models import Product, Brand, Category, ProductInventory, ProductType, ProductAttribute, ProductMedia, Stock
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
import pandas as pd
import string
from django.contrib.auth.models import User
from store.import_product import ImportProduct
from django.conf import settings


@login_required(login_url='authentication:sign-in')
@allowed_users(allowed_roles=['admin', 'seller', 'manager'])
def product_list(request):
    products = Product.objects.filter(user=request.user).values(
        'id', 'pid', 'title', 'thumbnail', 'product__store_price', 'product__upc', 'product__sku', 'product__is_active')
    context = {
        "products": products
    }
    return render(request, 'store/product/index.html', context)


@csrf_exempt
@login_required(login_url='authentication:sign-in')
@allowed_users(allowed_roles=['admin', 'seller', 'manager'])
def add_product_view(request):
    brands = Brand.objects.all()
    categories = Category.objects.all()
    users = User.objects.all()
    current_user = request.user
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        # titleData = request.POST['title']
        # brandData = Brand.objects.get(title=request.POST['brand'])
        # categoryData = Category.objects.get(name=request.POST['category'])
        # short_description = request.POST['short_description']
        # current_user = User.objects.get(username=request.POST['current_user'])
        # is_active_true = request.POST['is_active']
        # thumbnail = request.FILES['image']

        # # image upload
        # fs = FileSystemStorage()
        # filePath = fs.save(
        #     f'user-{request.user.id}/{thumbnail.name}', thumbnail)

        # data = Product(
        #     title=titleData,
        #     category=categoryData,
        #     description=short_description,
        #     user=current_user,
        #     thumbnail=filePath
        # )
        # data.save()
        return JsonResponse({'success': True})

    context = {
        "brands": brands,
        "categories": categories,
        "users": users,
        "current_user": current_user
    }
    return render(request, 'store/product/add-product.html', context)


def edit_product_view(request):
    product = Product.objects.get(pid=request.GET.get('pid'))
    print(product)    
    brands = Brand.objects.all()
    categories = Category.objects.all()
    users = User.objects.all()
    context = {
        "product": product,
        "brands": brands,
        "categories": categories,
        "users": users,
    }
    return render(request, "store/product/edit-product.html", context)


class ProductInventryView(View):
    def get(self, request, *args, **kwargs):
        inventries = ProductInventory.objects.all()
        print(inventries)
        context = {
            "inventries": inventries
        }
        # return render(request,"store/product/product-inventry.html",context)
        return JsonResponse({'success': True})


@method_decorator(csrf_exempt, name='dispatch')
class ProductImportView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "store/product/index.html")

    def post(self, request, *args, **kwargs):
        current_user = User.objects.get(username=self.request.user)

        fs = FileSystemStorage()
        products_file = request.FILES['products_file']
        # isExist = os.path.exists(filePath)
        # file = os.listdir(f"{settings.MEDIA_ROOT}/seller_csv-{request.user.id}")[0]
        # print("file name is====:",file)
        # filePath = os.path.join(f"{settings.MEDIA_ROOT}/seller_csv-{request.user.id}", products_file)
        filePath = f"{settings.MEDIA_ROOT}/seller_csv-{request.user.id}/{products_file}"
        if not os.path.exists(filePath):
            # print(filePath)
            filePath = fs.save(
                f'seller_csv-{request.user.id}/{products_file.name}', products_file)
        else:
            os.remove(filePath)
            filePath = fs.save(
                f'seller_csv-{request.user.id}/{products_file.name}', products_file)
        return JsonResponse({'status': 'success'})


################################ custom product import ############################################
@csrf_exempt
def custom_product_import(request):
    if request.method == 'POST':
        chunk_index = int(request.POST['step'])
        ################## product import start ############################
        dir_path = f"media/user-{request.user.id}"
        isExist = os.path.exists(dir_path)
        if not isExist:
            os.makedirs(dir_path)

        chunk_size = 50
        fileName = os.listdir(
            f"{settings.MEDIA_ROOT}/seller_csv-{request.user.id}")[0]
        filePath = f"{settings.MEDIA_ROOT}/seller_csv-{request.user.id}/{fileName}"
        product = ImportProduct(filePath, chunk_size, chunk_index)
        df = pd.read_csv(filePath, chunksize=chunk_size)
        chunk_list = product.total_chunk_list(df)
        total_chunk = len(chunk_list)

        for index in range(0, total_chunk):
            if index == chunk_index:
                currentChunk = chunk_list[index]
                print(currentChunk.info())
                for index, row in currentChunk.iterrows():
                    if row is not None:
                        product_sku = row['sku'].upper()
                        retail_price = row['retail_price']
                        product_weight = row['weight']
                        stock_price = row['stock_price']
                        stock_qty = row['stock_qty']
                        sale_price = row['sale_price']
                        images_media = row['media_images'].split(',')
                        ###### create brand ######
                        brand = row['brand']
                        if brand is not None:
                            brand_slug = brand.lower().replace(' ', '-')
                            # print(brand_slug)
                            c_and_u_brand = Brand.objects.filter(slug_url=brand_slug).update_or_create(
                                title=row['brand']
                            )
                        else:
                            print('=====brand is null======')
                        ###### create category ######
                        category_slug = row['category'].lower().replace(
                            ' & ', '-')
                        sub_category_slug = row['sub_category'].lower().replace(
                            ' & ', '-')
                        # print(category_slug)
                        category = Category.objects.filter(
                            slug=category_slug).order_by('id').first()
                        if category is None:
                            parent_cat = Category.objects.create(
                                name=row['category']
                            )
                            Category.objects.create(
                                name=row['sub_category'], parent=parent_cat)
                        else:
                            print("=====category already exist=====")

                        ###### create product type ######
                        prod_type = row['type']
                        if prod_type is not None:
                            product_type = prod_type.capitalize()
                            # print(product_type)
                            ProductType.objects.filter(title=product_type).update_or_create(
                                title=product_type
                            )
                        else:
                            print("=====product type is null=====")

                        ###### create and update product ######
                        product = Product.objects.filter(
                            title=row['title']).order_by('id').first()
                        if product is not None:
                            # print('update product')
                            Product.objects.filter(title=product).update(
                                title=row['title'],
                                category=category,
                                description=row['description'],
                                user=request.user,
                            )
                        else:
                            urls = row['thumbnail']
                            filename = urls.split('/')[-1]
                            file = urllib.request.urlretrieve(urls, os.path.join(
                                f"media/user-{request.user.id}/{filename}"))
                            new_file_path = f"user-{request.user.id}/{filename}"

                            # print('create product')
                            Product.objects.create(
                                title=row['title'],
                                category=category,
                                description=row['description'],
                                user=request.user,
                                thumbnail=new_file_path
                            )
                        ###### create and update inventry ######
                        p_title = Product.objects.filter(
                            title=row['title']).order_by('id').first()
                        product_sku = row['sku'].upper()
                        stock_keeping_unit = ProductInventory.objects.filter(
                            sku=product_sku).order_by('id').first()
                        if stock_keeping_unit is not None:
                            print("update inventry")
                            update_inventry = ProductInventory.objects.filter(sku=stock_keeping_unit).update(
                                product_type=ProductType.objects.filter(
                                    title=product_type).get(),
                                product=p_title,
                                brand=Brand.objects.filter(
                                    slug_url=brand.lower().replace(' ', '-')).get(),
                                retail_price=retail_price,
                                store_price=stock_price,
                                is_active=True,
                                is_digital=True,
                                weight=product_weight
                            )
                        else:
                            print("create inventry")
                            # str1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
                            # str2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
                            # str3 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
                            # generated_sku = f"{str1}-{str2}-{str3}"
                            upc_code = random.randint(
                                000000000000, 999999999999)
                            create_inventry = ProductInventory(
                                sku=product_sku,
                                upc=upc_code,
                                product_type=ProductType.objects.filter(
                                    title=product_type).get(),
                                product=p_title,
                                brand=Brand.objects.filter(
                                    slug_url=brand.lower().replace(' ', '-')).get(),
                                retail_price=retail_price,
                                store_price=stock_price,
                                is_active=True,
                                is_digital=True,
                                weight=product_weight
                            )
                            create_inventry.save()
                        ###### create and update stock ######
                        product_inventry = ProductInventory.objects.filter(
                            sku=product_sku).order_by('id').first()
                        update_stock = Stock.objects.filter(product_inventory=product_inventry).update_or_create(
                            product_inventory=product_inventry,
                            units=stock_qty,
                            units_sold=stock_qty
                        )
                        ###### create and update media ######
                        product_media_url = ProductMedia.objects.filter(
                            product_inventory=product_inventry).order_by('id').first()
                        if product_media_url is None:
                            print(product_media_url)
                            for url in images_media:
                                image_name = url.split('/')[-1]
                                file = urllib.request.urlretrieve(url, os.path.join(
                                    f"media/user-{request.user.id}/{image_name}"))
                                new_media_path = f"user-{request.user.id}/{image_name}"
                                insert_media = ProductMedia.objects.filter(product_inventory=product_inventry).update_or_create(
                                    product_inventory=product_inventry,
                                    img_url=new_media_path,
                                    alt_text=image_name,
                                )
                        else:
                            print("update images successfully")
                    else:
                        print('row value is null')

        print(chunk_index)
        ################## product import end ##############################
        chunk_index += 1
        if chunk_index >= total_chunk:
            chunk_index = 'completed'
            os.remove(filePath)
    return JsonResponse({'step': chunk_index, 'total_chunk': total_chunk})
