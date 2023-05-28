from tkinter import Widget
from django import forms
from django.core.exceptions import ValidationError
from App_Project.models import Task, Project, EmployeeTask, EmployeeProject
from App_User.models import Employee

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'start_date', 'end_date', 'manager')


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'start_date', 'end_date', 'project')
        # widgets = {'start_date': forms.DateTimeInput}

class EmployeeProjectForm(forms.ModelForm):
    class Meta:
        model = EmployeeProject
        fields = ('employees',)
        widgets = {'employees': forms.CheckboxSelectMultiple}
        

class EmployeeTaskForm(forms.ModelForm):
    class Meta:
        model = EmployeeTask
        fields = ('__all__')
        
        

class AssignTaskForm(forms.Form):
    employees = forms.ModelMultipleChoiceField(
        queryset=Employee.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Employees'
    )

    def __init__(self, *args, **kwargs):
        self.task = kwargs.pop('task')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        employees = cleaned_data.get('employees')
        if not employees:
            raise ValidationError('You must select at least one employee')
        for employee in employees:
            if employee in self.task.employees.all():
                raise ValidationError(f'{employee} is already assigned to this task')
        return cleaned_data
