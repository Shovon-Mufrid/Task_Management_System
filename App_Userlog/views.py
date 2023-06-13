from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserLog
# Create your views here.

@login_required
def user_log(request):
    user_logs = UserLog.objects.filter(user=request.user).order_by('-timestamp')[:10]
    context = {'user_logs': user_logs}
    return render(request, 'App_Userlog/log.html', context)