from django.contrib import admin
from .models import Subject, Test, Question, Submission, Mark, Comment

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_id', 'lesson_title', 'teacher')
    list_filter = ('teacher',)
    search_fields = ('lesson_title', 'description')

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('test_id', 'test_title', 'subject', 'start_time', 'end_time', 'is_open')
    list_filter = ('subject', 'start_time', 'end_time')
    search_fields = ('test_title', 'test_description')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'question_text', 'score', 'test')
    list_filter = ('test',)
    search_fields = ('question_text',)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('submission_id', 'student', 'question', 'teacher_score', 'ai_score')
    list_filter = ('student', 'question__test')
    search_fields = ('student__username', 'question__question_text')

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('mark_id', 'submission', 'teacher_mark', 'ai_mark', 'teacher')
    list_filter = ('teacher',)
    search_fields = ('submission__student__username',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'submission', 'teacher', 'comment_text')
    list_filter = ('teacher',)
    search_fields = ('submission__student__username',)
