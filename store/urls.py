from django.urls import path,re_path 
from store import views

app_name = "store"

urlpatterns = [
    re_path(r'^product-list/$',views.product_list,name="product-list"),
    re_path(r"add-product/$",views.add_product_view,name="add-product"),
    re_path(r"^edit-product/$",views.edit_product_view,name="edit-product"),
    re_path(r"^import-product/$",views.ProductImportView.as_view(),name="import-product"),
    re_path(r"^custom-product-import/$",views.custom_product_import,name="custom-product-import"),
    #brands
    re_path(r"^brand-list/$",views.brand_view,name="brand-list"),
    re_path(r"^add-brand/$",views.add_brand_view,name="add-brand"),
    path("edit-brand/<str:bid>/",views.edit_brand_view,name="edit-brand"),
    re_path(r"^delete-brand/$",views.delete_brand_view,name="delete-brand"),

    #category
    re_path(r"^category-list/$",views.category_view,name="category-list"),
    re_path(r"^add-category/$",views.add_category_view,name="add-category"), 
    re_path(r"^edit-category/$",views.edit_category_view,name="edit-category"),  
    re_path(r"^delete-category/$",views.delete_category_view,name="delete-category"),
]