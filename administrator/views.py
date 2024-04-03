from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.decorators import allowed_users
# Create your views here.

@login_required(login_url='authentication:sign-in')
@allowed_users(allowed_roles=['admin','seller','manager'])
def dashboard(request):
    return render(request,'dashboard/index.html')
