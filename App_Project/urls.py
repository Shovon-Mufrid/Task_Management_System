from django.urls import path
from App_Project import views

app_name = 'App_Project'

urlpatterns = [
    path('project/create/', views.create_project, name='create_project'),
    path('project/<int:pk>/update/', views.edit_project, name='update_project'),
    path('project/<int:pk>/delete/', views.delete_project, name='delete_project'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/<int:pk>/add_employee/', views.add_employee_to_project, name='add_employee_to_project'),
    path('project/<int:pk>/create_task/', views.create_task, name='create_task'),
    path('task/<int:pk>/update/', views.edit_task, name='edit_task'),
    path('task/<int:pk>/delete/', views.delete_task, name='delete_task'),
]