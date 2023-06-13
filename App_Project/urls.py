from django.urls import path
from App_Project import views

app_name = 'App_Project'

urlpatterns = [
    path('project/create/', views.create_project, name='create_project'),
    path('project/list/', views.ProjectList.as_view(), name='project_list'),
    path('project/<int:pk>/update/', views.edit_project, name='update_project'),
    path('project/<int:pk>/delete/', views.delete_project, name='delete_project'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/<int:project_pk>/create_task/', views.create_task, name='create_task'),
    path('task/<int:pk>/update/', views.edit_task, name='edit_task'),
    path('task/<int:pk>/delete/', views.delete_task, name='delete_task'),
    # path('tasks/<str:status>/', views.view_tasks_by_status, name='view_tasks_by_status'),
    # path('tasks/status/<str:status>/', views.view_tasks_by_status, name='view_tasks_by_status'),
    path('task/tasks-by-status/<str:status>/', views.tasks_by_status, name='tasks_by_status'),
    path('task/<int:task_id>/', views.task_details, name='task_details'),
    # path('task/<int:task_id>/add_employees/', views.add_employees_to_task, name='add_employees_to_task'),

]
