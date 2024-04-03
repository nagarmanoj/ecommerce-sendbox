from django.urls import path 
from landing import views


app_name = "landing"

urlpatterns = [
    path('',views.index,name="index"),
    # path('auth/sign-in',views.login_view,name="sign-in"),
    # path("sign-out/",views.logout_view,name="sign-out"),
]