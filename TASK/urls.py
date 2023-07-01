from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from App_User import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("App_User.urls")),
    path('userlog/', include('App_Userlog.urls')),
    path('project/', include('App_Project.urls')),
    
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "App_User.views.handle_not_found"