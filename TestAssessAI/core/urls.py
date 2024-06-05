from django.urls import path
from . import views

urlpatterns = [
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/add_subject/', views.add_subject, name='add_subject'),
    path('teacher/view_subject/<int:subject_id>/', views.view_subject, name='view_subject'),
    path('teacher/edit_subject/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('teacher/delete_subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),
    path('teacher/add_student_to_subject/<int:subject_id>/', views.add_student_to_subject, name='add_student_to_subject'),
    path('teacher/add_test_to_subject/<int:subject_id>/', views.add_test_to_subject, name='add_test_to_subject'),
    path('teacher/view_test/<int:test_id>/', views.view_test, name='view_test'),
    path('teacher/edit_test/<int:test_id>/', views.edit_test, name='edit_test'),
    path('teacher/delete_test/<int:test_id>/', views.delete_test, name='delete_test'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/add_question_to_test/<int:test_id>/', views.add_question_to_test, name='add_question_to_test'),
    path('teacher/edit_question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('teacher/delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('student/view_test/<int:test_id>/', views.view_test_student, name='view_test_student'),

]
