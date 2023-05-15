from django.contrib import admin
from App_Project import models
# Register your models here.

admin.site.register(models.Project)
admin.site.register(models.Task)
admin.site.register(models.CompletedTask)
admin.site.register(models.IncompletedTask)
admin.site.register(models.AssignedTask)
admin.site.register(models.WorkingTask)
admin.site.register(models.EmployeeTask)
