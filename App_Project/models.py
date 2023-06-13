from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from App_User.models import Employee, UserProfile


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    manager = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='managed_projects')
    employees = models.ManyToManyField(Employee, related_name='projects')

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = (
        ('ASSIGNED', 'Assigned'),
        ('WORKING', 'Working'),
        ('COMPLETED', 'Completed'),
        ('INCOMPLETED', 'Incompleted'),
    )
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name = 'tasks')
    assigned_to = models.ManyToManyField(Employee, related_name='assigned_tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ASSIGNED')
    completed_by = models.ManyToManyField(Employee, related_name='completed_tasks', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class CompletedTask(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, primary_key=True)

class AssignedTask(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, primary_key=True)

class WorkingTask(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, primary_key=True)

class IncompletedTask(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, primary_key=True)



# class CompletedTask(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#     completed_by = models.ForeignKey(Employee, on_delete=models.CASCADE)
#     completed_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.task.name


# class IncompletedTask(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.task.name


# class AssignedTask(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#     assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.task.name


# class WorkingTask(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#     assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.task.name

class EmployeeProject(models.Model):
    employees = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.employees} - {self.project}'


class EmployeeTask(models.Model):
    employee_project = models.ForeignKey(EmployeeProject, on_delete=models.CASCADE)
    employees = models.ForeignKey(Employee, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.employees} - {self.task}'
