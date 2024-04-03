from django.contrib import admin
from store.models import *
from mptt.admin import DraggableMPTTAdmin

#Product Table
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','pid','title','slug','thumbnail']
    readonly_fields=['slug']
admin.site.register(Product,ProductAdmin)
#Category Table
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    readonly_fields=['slug']
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'
admin.site.register(Category,CategoryAdmin)
#Brand Table
class BrandAdmin(admin.ModelAdmin):
    list_display=["id","title","slug_url","thumbnail"]
    readonly_fields=['slug_url']
admin.site.register(Brand,BrandAdmin)
#ProductType Table
admin.site.register(ProductType)
admin.site.register(ProductAttribute)
#Stock Table
class StockAdmin(admin.ModelAdmin):
    list_display=["id","product_inventory","last_checked","units","units_sold"]
admin.site.register(Stock,StockAdmin)
#ProductMedia Table
class ProductMediaAdmin(admin.ModelAdmin):
    list_display=["id","product_inventory","img_url","alt_text","is_feature","created_at","updated_at"]
admin.site.register(ProductMedia,ProductMediaAdmin)

admin.site.register(ProductAttributeValues)
admin.site.register(ProductTypeAttribute)
#inventry
class StoreAdmin(admin.ModelAdmin):
    list_display = ("id","sku","upc","product","retail_price", "store_price","weight","created_at","updated_at")



admin.site.register(ProductInventory, StoreAdmin)

#cart table
class CartAdmin(admin.ModelAdmin):
    list_display=["id","user"]
admin.site.register(Cart,CartAdmin)

#cart Items
class CartItemAdmin(admin.ModelAdmin):
    list_display=["id","cart","product","quantity","price","total_price"]
admin.site.register(CartItem,CartItemAdmin)
