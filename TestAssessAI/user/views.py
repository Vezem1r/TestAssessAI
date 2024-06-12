from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import StudentLoginForm, TeacherLoginForm, StudentRegistrationForm, TeacherRegistrationForm
from .models import User

def index(request):
    return render(request, 'index.html')

def student_login(request):
    error_message = None
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.role == User.Role.STUDENT:
                login(request, user)
                return redirect('student_dashboard')
            else:
                error_message = 'Invalid username or password.'
    else:
        form = StudentLoginForm()
    return render(request, 'student_login.html', {'form': form, 'error_message': error_message})

def teacher_login(request):
    error_message = None
    if request.method == 'POST':
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.role == User.Role.TEACHER:
                login(request, user)
                return redirect('teacher_dashboard')
            else:
                error_message = 'Invalid username or password.'
    else:
        form = TeacherLoginForm()
    return render(request, 'teacher_login.html', {'form': form, 'error_message': error_message})


def student_registration(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.Role.STUDENT
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('student_dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'student_registration.html', {'form': form})

def teacher_registration(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.Role.TEACHER
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('teacher_dashboard')
    else:
        form = TeacherRegistrationForm()
    return render(request, 'teacher_registration.html', {'form': form})

def student_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_student():
        return redirect('student_login')
    return render(request, 'student_dashboard.html')

def teacher_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_teacher():
        return redirect('teacher_login')
    return render(request, 'teacher_dashboard.html')

def user_logout(request):
    logout(request)
    return redirect('index')
