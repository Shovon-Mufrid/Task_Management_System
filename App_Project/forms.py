from tkinter import Widget
from django import forms
from django.core.exceptions import ValidationError
from App_Project.models import Task, Project, EmployeeTask, EmployeeProject
from App_User.models import Employee
# from django.contrib.admin.widgets import AdminDateWidget
from tempus_dominus.widgets import DateTimePicker
from django.forms import DateInput, DateTimeInput


class ProjectForm(forms.ModelForm):
    # start_date = forms.DateField(widget=AdminDateWidget)
    # start_date = forms.DateTimeField(widget=DateTimePicker)
    class Meta:
        model = Project
        fields = ('name', 'description', 'start_date', 'end_date', 'manager')
        widgets = {
            'start_date': DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'end_date': DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            # 'start_date': DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
            # 'end_date': DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
            }
        
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # fields = ('__all__')
        exclude = ('completed_by',)
        widgets = {
            'start_date': DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'end_date': DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            }
        
class EmployeeProjectForm(forms.ModelForm):
    class Meta:
        model = EmployeeProject
        fields = ('employees',)
        widgets = {'employees': forms.CheckboxSelectMultiple}
        

class EmployeeTaskForm(forms.ModelForm):
    class Meta:
        model = EmployeeTask
        fields = ['employees']
        
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
