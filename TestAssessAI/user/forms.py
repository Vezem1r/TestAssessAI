from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class StudentLoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class TeacherLoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        def clean_password2(self):
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Passwords do not match")
            if len(password1) < 8:
                raise forms.ValidationError("Password is too short (minimum 8 characters)")
            if not any(char.isdigit() for char in password1):
                raise forms.ValidationError("Password must contain at least one digit")
            if not any(char.isalpha() for char in password1):
                raise forms.ValidationError("Password must contain at least one letter")
            return password2

class TeacherRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        def clean_password2(self):
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Passwords do not match")
            if len(password1) < 8:
                raise forms.ValidationError("Password is too short (minimum 8 characters)")
            if not any(char.isdigit() for char in password1):
                raise forms.ValidationError("Password must contain at least one digit")
            if not any(char.isalpha() for char in password1):
                raise forms.ValidationError("Password must contain at least one letter")
            return password2
