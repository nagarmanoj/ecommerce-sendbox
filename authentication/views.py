from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from authentication.form import UserRegisterForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from authentication.decorators import allowed_users
# Create your views here.
def register_view(request):
    if request.method == "POST":
        # print(" User register")
        # print(request.POST)
        form  = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            # create group
            group = Group.objects.get(name="customer")
            new_user.groups.add(group)
            username = form.cleaned_data.get("username")
            messages.success(request,f"Hey {username}, You account created successfully")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1']                                    
            )
            login(request,new_user)
            print("User register Successfully!")
            return redirect("landing:index")
    else:
        print("User not register")
        form  = UserRegisterForm()
    context = {
        'form':form
    }
    return render(request,'auth/sign_up.html',context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request,f"Hey you are already logged in")
        return redirect("landing:index")
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
        try:
            username = User.objects.get(email=email.lower()).username
            user = authenticate(request,username=username, password=password)
            print(user)
            if user is not None:
                login(request,user)
                messages.success(request,"You are logged in")
                # return redirect("landing:index")
                return JsonResponse({'success':True})
            else:
                messages.warning(request,"User does not exist create an account.")
        except:
            messages.warning(request,f"User with {email} does not exist")

    return render(request,'auth/sign_in.html')

def logout_view(request):
    logout(request)
    messages.success(request,"You logged out")
    return redirect("authentication:sign-in")



# ##########################################User Administration####################################
@login_required(login_url='authentication:sign-in')
@allowed_users(allowed_roles=['admin','seller','manager'])
def user_list_view(request):
    users = User.objects.all()
    context = {
        'users':users
    }
    return render(request,'users/users-list.html',context)

@login_required(login_url='authentication:sign-in')
@allowed_users(allowed_roles=['admin','seller','manager'])
def user_setting_view(request):
    return render(request,'setting/user-setting.html')