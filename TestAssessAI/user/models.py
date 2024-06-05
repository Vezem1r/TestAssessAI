from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        STUDENT = "STUDENT", 'Student'
        TEACHER = "TEACHER", 'Teacher'
        
    base_role = Role.ADMIN
    
    role = models.CharField(max_length=50, choices=Role.choices)
    
    def is_student(self):
        return self.role == self.Role.STUDENT
    
    def is_teacher(self):
        return self.role == self.Role.TEACHER


class Student(User):
    base_role = User.Role.STUDENT
    
    
    class Meta:
        proxy = True
    


class Teacher(User):
    base_role = User.Role.TEACHER
    
    
    class Meta:
        proxy = True
    

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.IntegerField(null=True, blank=True)


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.IntegerField(null=True, blank=True)
