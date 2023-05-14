from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Employee

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['__all__']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['__all__']