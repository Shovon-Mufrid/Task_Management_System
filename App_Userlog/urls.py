from django.urls import path
from App_Userlog import views

app_name = 'App_Userlog'

urlpatterns = [
  path('log/', views.user_log, name='userlog'),
    ]