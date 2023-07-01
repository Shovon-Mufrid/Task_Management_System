from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Project, Task, EmployeeTask, CompletedTask, IncompletedTask, AssignedTask, WorkingTask
from App_User.models import Employee
from .forms import ProjectForm, TaskForm, EmployeeTaskForm, AssignTaskForm
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, UpdateView, ListView, DetailView, View, TemplateView, DeleteView
# import datetime
from datetime import datetime

class ProjectList(ListView):
    context_object_name = 'projects'
    model = Project
    template_name = 'App_Project/project_list.html'
    # queryset = Blog.objects.order_by('-publish_date')

@login_required
def project_detail(request, pk):
    """
    Displays the details of a project, along with the tasks associated with it
    """
    project = get_object_or_404(Project, pk=pk)

    tasks = Task.objects.filter(project=project)
    assigned_count = project.tasks.filter(status='ASSIGNED').count()
    working_count = project.tasks.filter(status='WORKING').count()
    completed_count = project.tasks.filter(status='COMPLETED').count()
    incompleted_count = project.tasks.filter(status='INCOMPLETED').count()

    # Countdown
    # remaining_days = (project.end_date - datetime.date.today()).days
    # remaining_time =  str(project.end_date - datetime.datetime.now().date())
    # remaining_time = project.time_remaining().days * 24 * 60 * 60 

    context = {'project': project, 'tasks': tasks,
                'assigned_count': assigned_count,
                'working_count': working_count,
                'completed_count': completed_count,
                'incompleted_count': incompleted_count,
                # 'remaining_days': remaining_days,
                # 'remaining_time': remaining_time,
                
            
               }
    return render(request, 'App_Project/project_detail.html', context)


@login_required
def create_project(request):
    """
    Allows the admin to create a new project
    """
    managers = Employee.objects.filter(managed_projects=True)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.admin = request.user
            # project.manager = Employee.objects.get(user=request.POST.get('manager'))
            # project.manager = request.user.employee
            project.save()
            form.save_m2m()
            messages.success(request, 'Project created successfully')
            return redirect('App_Project:project_detail', pk=project.pk)
    else:
        form = ProjectForm()

    context = {'form': form, 'managers': managers}
    return render(request, 'App_Project/create_project.html', context)


@login_required
def edit_project(request, pk):
    """
    Allows the admin to edit an existing project
    """
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully')
            return redirect('App_Project:project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)

    context = {'form': form, 'project': project}
    return render(request, 'App_Project/edit_project.html', context)

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    messages.success(request, 'Project has been deleted successfully!')
    return redirect('App_Project:project_list')

@login_required
def create_task(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, 'Task created successfully')
            return redirect('App_Project:project_detail', pk=project.pk)
    else:
        form = TaskForm()

    context = {'form': form, 'project': project}
    return render(request, 'App_Project/create_task.html', context)

@login_required
def edit_task(request, pk):
    """
    Allows the admin or project manager to edit an existing task for a project
    """
    task = get_object_or_404(Task, pk=pk)
    project = task.project

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save() 
            form.save_m2m() 
            messages.success(request, 'Task updated successfully')
            return redirect('App_Project:project_detail', pk=project.pk)
            # form.save()
            # messages.success(request, 'Task updated successfully')
            # return redirect('App_Project:project_detail', pk=project.pk)
    else:
        form = TaskForm(instance=task)

    context = {'form': form, 'project': project, 'task': task}
    return render(request, 'App_Project/edit_task.html', context)

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project_pk = task.project.pk  # Retrieve the project's primary key for redirection

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task has been deleted successfully!')
        return redirect('App_Project:project_detail', pk=project_pk)

    context = {'task': task}
    return render(request, 'App_Project/delete_task.html', context)

@login_required
def assign_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project
    if request.user.is_superuser or request.user == project.manager:
        if request.method == 'POST':
            form = AssignTaskForm(request.POST)
            if form.is_valid():
                employees = form.cleaned_data.get('employees')
                task.employees.add(*employees)
                task.status = Task.Status.ASSIGNED
                task.save()
                messages.success(request, 'Task assigned successfully')
                return redirect('project_detail', project.pk)
            else:
                form = AssignTaskForm()
            return render(request, 'App_Project/assign_task.html', {'form': form, 'task': task})
        else:
            raise PermissionDenied


@login_required
def delete_task(request, pk):
    """
    Allows the admin or project manager to delete a task for a project
    """
    task = get_object_or_404(Task, pk=pk)
    project = task.project

    if request.user.is_superuser or request.user == project.manager:
        if request.method == 'POST':
            task.delete()
            messages.success(request, 'Task deleted successfully')
            return redirect('App_Project:project_detail', pk=project.pk)
        else:
            return render(request, 'App_Project/delete_task.html', {'task': task})
    else:
        raise PermissionDenied

@login_required
def tasks_by_status(request, status):
    tasks = Task.objects.filter(status=status)
    task_count = tasks.count()
    return render(request, 'App_Project/tasks_by_status.html', {'tasks': tasks, 'status': status,  'task_count': task_count})


# @login_required
# def change_task_status(request, pk, status):

#     task = get_object_or_404(Task, pk=pk)

#     valid_statuses = ['completed', 'assigned', 'working', 'incompleted']
#     if status not in valid_statuses:
#         raise Http404

#     if status == 'completed':
#         task.status = Task.Status.COMPLETED
#         CompletedTask.objects.create(task=task)
#     elif status == 'assigned':
#         task.status = Task.Status.ASSIGNED
#         AssignedTask.objects.create(task=task)
#     elif status == 'working':
#         task.status = Task.Status.WORKING
#         WorkingTask.objects.create(task=task)
#     elif status == 'incompleted':
#         task.status = Task.Status.INCOMPLETED
#         IncompletedTask.objects.create(task=task)

#     task.save()
#     messages.success(request, 'Task status updated successfully')
#     return redirect('App_Project:view_tasks_by_status', status=status)



# @login_required
# def view_tasks_by_status(request, status):
#     """
#     Displays tasks based on their status (Completed, Assigned, Working, Incompleted)
#     """
#     valid_statuses = ['completed', 'assigned', 'working', 'incompleted']
#     if status not in valid_statuses:
#         raise Http404

#     tasks = []
#     if status == 'completed':
#         tasks = CompletedTask.objects.select_related('task')
#     elif status == 'assigned':
#         tasks = AssignedTask.objects.select_related('task')
#     elif status == 'working':
#         tasks = WorkingTask.objects.select_related('task')
#     elif status == 'incompleted':
#         tasks = IncompletedTask.objects.select_related('task')

#     context = {'tasks': tasks, 'status': status}
#     return render(request, 'App_Project/tasks_by_status.html', context)



def task_details(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    context = {'task': task}
    return render(request, 'App_Project/task_details.html', context)

# def add_employees_to_task(request, task_id):
#     task = get_object_or_404(Task, pk=task_id)
#     if request.method == 'POST':
#         # form = TaskForm(request.POST, instance=task)
#         form = EmployeeTaskForm(request.POST)
#         if form.is_valid():
#             employee_task = form.save(commit=False)
#             employee_task.task = task
#             employee_task.save()
#             return redirect('App_Project:task_details', task_id=task_id)
#     else:
#          form = EmployeeTaskForm()
#     context = {'form': form, 'task': task}
#     return render(request, 'App_Project/add_employees_to_task.html', context)
