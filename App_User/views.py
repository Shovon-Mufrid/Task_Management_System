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

@login_required
def profile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    return render(request, 'App_User/profile.html', {'user': user, 'profile': profile})


# @login_required
# def profile_view(request):
#     profiles = request.user.profile
#     return render(request, 'App_User/profile.html', context={'profiles': profiles})

# @login_required
# def edit_profile(request):
#     current_user =  Profile.objects.get(user=request.user)
#     form = UserProfileForm(instance=current_user)
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES, instance=current_user)
#         if form.is_valid():
#             form.save(commit=True)
#             form = UserProfileForm(instance=current_user)
#             return HttpResponseRedirect(reverse('App_User:profile'))
#     return render(request, "App_User/profile_edit.html", context={'form': form})  