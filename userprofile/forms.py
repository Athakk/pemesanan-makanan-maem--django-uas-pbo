from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control my-2'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control my-2'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input my-2'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input my-2'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input my-2'}),
        }
