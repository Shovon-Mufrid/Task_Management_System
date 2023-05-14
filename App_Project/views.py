from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Project, Task, EmployeeTask
from .forms import ProjectForm, TaskForm, EmployeeTaskForm, AssignTaskForm
from django.core.exceptions import PermissionDenied


@login_required
def project_list(request):
    """
    Displays the list of projects for the logged in user
    """
    projects = Project.objects.filter(employees=request.user.employee)

    context = {'projects': projects}
    return render(request, 'project_list.html', context)


@login_required
def project_detail(request, pk):
    """
    Displays the details of a project, along with the tasks associated with it
    """
    project = get_object_or_404(Project, pk=pk)

    tasks = Task.objects.filter(project=project)

    context = {'project': project, 'tasks': tasks}
    return render(request, 'project_detail.html', context)


@login_required
def create_project(request):
    """
    Allows the admin to create a new project
    """
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.admin = request.user
            project.save()
            form.save_m2m()
            messages.success(request, 'Project created successfully')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()

    context = {'form': form}
    return render(request, 'create_project.html', context)


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
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)

    context = {'form': form, 'project': project}
    return render(request, 'edit_project.html', context)


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
            return redirect('project_detail', pk=pk)
    else:
        form = TaskForm()

    context = {'form': form, 'project': project}
    return render(request, 'create_task.html', context)


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
            return redirect('project_detail', pk=project.pk)
    else:
        form = TaskForm(instance=task)

    context = {'form': form, 'project': project, 'task': task}
    return render(request, 'edit_task.html', context)


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
            return render(request, 'app_project/assign_task.html', {'form': form, 'task': task})
        else:
            raise PermissionDenied






# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.utils import timezone
# from .models import Project, Task, EmployeeTask
# from .forms import ProjectForm, TaskForm, EmployeeTaskForm
# from django.core.exceptions import PermissionDenied


# @login_required
# def project_list(request):
#     """
#     Displays the list of projects for the logged in user
#     """
#     projects = Project.objects.filter(employees=request.user.employee)

#     context = {'projects': projects}
#     return render(request, 'project_list.html', context)


# @login_required
# def project_detail(request, pk):
#     """
#     Displays the details of a project, along with the tasks associated with it
#     """
#     project = get_object_or_404(Project, pk=pk)

#     tasks = Task.objects.filter(project=project)

#     context = {'project': project, 'tasks': tasks}
#     return render(request, 'project_detail.html', context)


# @login_required
# def create_project(request):
#     """
#     Allows the admin to create a new project
#     """
#     if request.method == 'POST':
#         form = ProjectForm(request.POST)
#         if form.is_valid():
#             project = form.save(commit=False)
#             project.admin = request.user
#             project.save()
#             form.save_m2m()
#             messages.success(request, 'Project created successfully')
#             return redirect('project_detail', pk=project.pk)
#     else:
#         form = ProjectForm()

#     context = {'form': form}
#     return render(request, 'create_project.html', context)


# @login_required
# def edit_project(request, pk):
#     """
#     Allows the admin to edit an existing project
#     """
#     project = get_object_or_404(Project, pk=pk)

#     if request.method == 'POST':
#         form = ProjectForm(request.POST, instance=project)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Project updated successfully')
#             return redirect('project_detail', pk=pk)
#     else:
#         form = ProjectForm(instance=project)

#     context = {'form': form, 'project': project}
#     return render(request, 'edit_project.html', context)


# @login_required
# def create_task(request, pk):
#     """
#     Allows the admin or project manager to create a new task for a project
#     """
#     project = get_object_or_404(Project, pk=pk)

#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             task = form.save(commit=False)
#             task.project = project
#             task.save()
#             form.save_m2m()
#             messages.success(request, 'Task created successfully')
#             return redirect('project_detail', pk=pk)
#     else:
#         form = TaskForm()

#     context = {'form': form, 'project': project}
#     return render(request, 'create_task.html', context)


# @login_required
# def edit_task(request, pk):
#     """
#     Allows the admin or project manager to edit an existing task for a project
#     """
#     task = get_object_or_404(Task, pk=pk)
#     project = task.project

#     if request.method == 'POST':
#         form = TaskForm(request.POST, instance=task)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Task updated successfully')
#             return redirect('project_detail', pk=project.pk)
#     else:
#         form = TaskForm(instance=task)

#     context = {'form': form, 'project': project, 'task': task}
#     return render(request, 'edit_task.html', context)