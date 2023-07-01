from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserLog
from django.core.paginator import Paginator

# Create your views here.

@login_required
def user_log(request):
    # user_logs = UserLog.objects.filter(user=request.user).order_by('-timestamp')[:10]
    user_log = UserLog.objects.filter(user=request.user).order_by('-timestamp')
    paginator = Paginator(user_log, 10)
    page = request.GET.get('page') 
    user_logs = paginator.get_page(page)
    context = {'user_logs': user_logs}
    return render(request, 'App_Userlog/log.html', context)

