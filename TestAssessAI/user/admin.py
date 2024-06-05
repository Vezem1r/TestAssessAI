from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, TeacherProfile


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom Fields', {'fields': ('role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'role'),
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Student Profiles'


class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile
    can_delete = False
    verbose_name_plural = 'Teacher Profiles'


class UserProfileAdmin(CustomUserAdmin):
    inlines = (StudentProfileInline, TeacherProfileInline,)


admin.site.register(User, UserProfileAdmin)
