from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('App_User:home')
        else:
            # messages.error(request, 'Invalid login credentials')
            error_message = 'Invalid email or password. Please try again.'
            return render(request, 'App_User/login.html', {'error_message': error_message })
    else:
        return render(request, 'App_User/login.html')

def user_logout(request):
    logout(request)
    return redirect('App_User:login')

@login_required
def home(request):
    return render(request, 'App_User/home.html')


def profile(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'App_User/profile.html', {'user': user})

