from django.db import models
from user.models import Teacher, Student
from ckeditor.fields import RichTextField
from django.db.models import Sum
from django.utils import timezone

class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    lesson_title = models.CharField(max_length=50)
    description = models.TextField(max_length=1024)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='subjects', blank=True)
    
class Test(models.Model):
    test_id = models.AutoField(primary_key=True)
    test_title = models.CharField(max_length=50)
    test_description = models.TextField(max_length=1024)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField(default=60) 
    max_score = models.FloatField(default=100.0)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    is_open = models.BooleanField(default=False)
    
    @property
    def total_score(self):
        submissions = Submission.objects.filter(question__test=self)
        total_teacher_score = submissions.aggregate(Sum('mark__teacher_mark'))['mark__teacher_mark__sum'] or 0
        total_ai_score = submissions.aggregate(Sum('mark__ai_mark'))['mark__ai_mark__sum'] or 0
        return total_teacher_score + total_ai_score

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_text = RichTextField()
    score = models.FloatField()
    max_length = models.IntegerField(default=500)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.question_text

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_text = models.TextField(max_length=256)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    submission = models.ForeignKey('Submission', on_delete=models.CASCADE,default=1)

class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    question_answer = models.TextField(max_length=5000, default="None")
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    @property
    def teacher_score(self):
        return self.mark_set.aggregate(models.Sum('teacher_mark'))['teacher_mark__sum'] or 0
        
    @property
    def ai_score(self):
        return self.mark_set.aggregate(Sum('ai_mark'))['ai_mark__sum'] or 0

class Mark(models.Model):
    mark_id = models.AutoField(primary_key=True)
    ai_mark = models.FloatField(default=0)  
    teacher_mark = models.FloatField(default=0)  
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)