from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('student/login/', views.student_login, name='student_login'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('student/registration/', views.student_registration, name='student_registration'),
    path('teacher/registration/', views.teacher_registration, name='teacher_registration'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('logout/', views.user_logout, name='logout'),
]
