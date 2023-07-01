from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from App_User.models import Employee, UserProfile
from datetime import datetime


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    manager = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='managed_projects')
    employees = models.ManyToManyField(Employee, related_name='projects')

    def __str__(self):
        return self.name
    
    def time_remaining(self):
        current_time = datetime.now().date()
        remaining_time = self.end_date - current_time
        return remaining_time

    def time_remaining_days(self):
        remaining_time = self.time_remaining()
        return remaining_time.days

    def time_remaining_hours(self):
        remaining_time = self.time_remaining()
        total_seconds = remaining_time.total_seconds()
        hours = total_seconds // 3600
        return int(hours)

    def time_remaining_minutes(self):
        remaining_time = self.time_remaining()
        total_seconds = remaining_time.total_seconds()
        minutes = (total_seconds % 3600) // 60
        return int(minutes)

    def time_remaining_seconds(self):
        remaining_time = self.time_remaining()
        total_seconds = remaining_time.total_seconds()
        seconds = total_seconds % 60
        return int(seconds)


class Task(models.Model):
    STATUS_CHOICES = (
        ('ASSIGNED', 'Assigned'),
        ('WORKING', 'Working'),
        ('COMPLETED', 'Completed'),
        ('INCOMPLETED', 'Incompleted'),
    )
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)
    # start_date = models.DateField()
    # end_date = models.DateField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
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

class EmployeeProject(models.Model):
    employees = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.employees} - {self.project}'


class EmployeeTask(models.Model):
    employee_project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    employees = models.ForeignKey(Employee, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.employees} - {self.task} - {self.employee_project}'




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