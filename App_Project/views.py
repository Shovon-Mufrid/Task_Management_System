from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Project, Task, EmployeeTask
from App_User.models import Employee
from .forms import ProjectForm, TaskForm, EmployeeTaskForm, AssignTaskForm
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, UpdateView, ListView, DetailView, View, TemplateView, DeleteView

# @login_required
# def project_list(request):
#     """
#     Displays the list of projects for the logged in user
#     """
#     projects = Project.objects.filter(employees=request.user.employee)

#     context = {'projects': projects}
#     return render(request, 'App_Project/project_list.html', context)

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

    context = {'project': project, 'tasks': tasks}
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

# @login_required
# def add_employee_to_project(request, pk):
#     project = get_object_or_404(Project, pk=pk)
#     if request.method == 'POST':
#         form = EmployeeTaskForm(request.POST)
#         if form.is_valid():
#             employee_task = form.save(commit=False)
#             employee_task.project = project
#             employee_task.save()
#             messages.success(request, 'Employee has been added to project successfully!')
#             return redirect('App_Project:project_detail', pk=project.pk)
#     else:
#         form = EmployeeTaskForm()
#     return render(request, 'App_Project/add_employee.html', {'form': form, 'project': project})


# @login_required
# def add_employee_to_project(request, project_id):
#     project = get_object_or_404(Project, id=project_id)

#     if request.method == 'POST':
#         employees = request.POST.getlist('employees')
#         for employee in employees:
#             EmployeeTask.objects.create(employees=Employee.objects.get(id=employee), task=project)
#         messages.success(request, 'Employees added to the project successfully')
#         return redirect('App_Project:project_detail', pk=project.pk)

#     context = {
#         'project': project,
#         'employees': Employee.objects.all(),  # Or you can customize this queryset as per your needs
#     }
#     return render(request, 'App_Project/add_employee_to_project.html', context)




@login_required
def create_task(request, pk):
    """
    Allows the admin or project manager to create a new task for a project
    """
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            form.save_m2m()
            messages.success(request, 'Task created successfully')
            return redirect('App_Project:project_detail', pk=pk)
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
            form.save()
            messages.success(request, 'Task updated successfully')
            return redirect('App_Project:project_detail', pk=project.pk)
    else:
        form = TaskForm(instance=task)

    context = {'form': form, 'project': project, 'task': task}
    return render(request, 'App_Project/edit_task.html', context)


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
