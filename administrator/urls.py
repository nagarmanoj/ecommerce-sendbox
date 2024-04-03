from django.urls import path,re_path,include
from administrator import views


app_name = "administrator"

urlpatterns = [    
    path('dashboard',views.dashboard,name="dashboard"),
    
    
]