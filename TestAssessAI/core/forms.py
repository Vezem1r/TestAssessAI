from django import forms
from .models import Question, Test, Submission
from ckeditor.widgets import CKEditorWidget

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'score']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'score', 'max_length']
        widgets = {
            'question_text': CKEditorWidget(),
        }
        
class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['test_title', 'test_description', 'start_time', 'end_time', 'duration', 'max_score']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        duration = cleaned_data.get("duration")

        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError("End time must be after start time.")

        if start_time and duration:
            if duration <= 0:
                raise forms.ValidationError("Duration must be a positive number.")

        return cleaned_data
    
class TestSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['question_answer']