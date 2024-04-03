from django.urls import path 
from authentication import views

app_name = "authentication"

urlpatterns = [    
    path('sign-in',views.login_view,name="sign-in"),
    path("sign-up/",views.register_view,name="sign-up"),
    path("sign-out/",views.logout_view,name="sign-out"),

    path('users/',views.user_list_view,name="users"),
    path('user-setting/',views.user_setting_view,name="user-setting"),
]