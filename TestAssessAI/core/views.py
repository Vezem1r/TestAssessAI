from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Subject, Test, Question, Submission
from user.models import User, Student
from django.contrib.auth import get_user_model
from .forms import QuestionForm, TestForm, TestSubmissionForm
from django.urls import reverse
from django.utils import timezone
from django.db.models import Sum

@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher():
        return redirect('index')
    subjects = Subject.objects.filter(teacher=request.user)
    return render(request, 'core/teacher_dashboard.html', {'subjects': subjects})

@login_required
def add_subject(request):
    if request.method == 'POST' and request.user.is_teacher():
        title = request.POST.get('title')
        description = request.POST.get('description')
        Subject.objects.create(lesson_title=title, description=description, teacher=request.user)
        return redirect('teacher_dashboard')
    return render(request, 'core/add_subject.html')

@login_required
def delete_subject(request, subject_id):
    if request.user.is_teacher():
        try:
            subject = Subject.objects.get(pk=subject_id, teacher=request.user)
            subject.delete()
        except Subject.DoesNotExist:
            pass
    return redirect('teacher_dashboard')

@login_required
def edit_subject(request, subject_id):
    if request.user.is_teacher():
        try:
            subject = Subject.objects.get(pk=subject_id, teacher=request.user)
            if request.method == 'POST':
                subject.lesson_title = request.POST.get('title')
                subject.description = request.POST.get('description')
                subject.save()
                return redirect('teacher_dashboard')
            return render(request, 'core/edit_subject.html', {'subject': subject})
        except Subject.DoesNotExist:
            pass
    return redirect('teacher_dashboard')

@login_required
def add_student_to_subject(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id, teacher=request.user)
    if request.method == 'POST' and request.user.is_teacher():
        student_ids = request.POST.getlist('students')
        selected_students = Student.objects.filter(id__in=student_ids)
        subject.students.set(selected_students)
        return redirect('view_subject', subject_id=subject_id)
    
    User = get_user_model()
    all_students = User.objects.filter(role=User.Role.STUDENT)
    subject_students = subject.students.all()
    return render(request, 'core/add_student_to_subject.html', {
        'subject': subject,
        'all_students': all_students,
        'subject_students': subject_students
    })

@login_required
def add_test_to_subject(request, subject_id):
    if request.method == 'POST' and request.user.is_teacher():
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.subject_id = subject_id
            test.save()
            subject_url = reverse('view_subject', kwargs={'subject_id': subject_id})
            return redirect(subject_url)
    else:
        form = TestForm()

    return render(request, 'core/add_test_to_subject.html', {'form': form, 'subject_id': subject_id})

@login_required
def student_dashboard(request):
    if not request.user.is_student():
        return redirect('index')
    
    now = timezone.localtime(timezone.now())
    
    subjects = Subject.objects.filter(students=request.user)
    subject_tests = []
    
    for subject in subjects:
        tests = Test.objects.filter(subject=subject)
        for test in tests:
            test.is_open = test.start_time <= now <= test.end_time
            test.save()
        total_score = 0
        for test in tests:
            submissions = Submission.objects.filter(student=request.user, question__test=test)
            total_score += submissions.aggregate(Sum('mark__teacher_mark'))['mark__teacher_mark__sum'] or 0
        
        subject_tests.append({'subject': subject, 'tests': tests, 'total_score': total_score})
    
    return render(request, 'core/student_dashboard.html', {'subject_tests': subject_tests, 'now': now})

@login_required
def view_subject(request, subject_id):
    if not request.user.is_teacher():
        return redirect('index')
    try:
        subject = Subject.objects.get(pk=subject_id, teacher=request.user)
        all_students = User.objects.filter(role=User.Role.STUDENT)
    except Subject.DoesNotExist:
        return redirect('teacher_dashboard')
    return render(request, 'core/view_subject.html', {'subject': subject, 'students': all_students})

@login_required
def view_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    return render(request, 'core/view_test.html', {'test': test})

@login_required
def edit_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    if request.method == 'POST':
        form = TestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            return redirect('view_subject', subject_id=test.subject.pk)  
    else:
        form = TestForm(instance=test)
    return render(request, 'core/edit_test.html', {'form': form, 'test': test})

@login_required
def delete_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    subject_id = test.subject.subject_id
    test.delete()
    return redirect('view_subject', subject_id=subject_id)

@login_required
def add_question_to_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    if request.method == 'POST' and request.user.is_teacher():
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.test = test
            question.save()
            return redirect('view_test', test_id=test_id)
    else:
        form = QuestionForm()
    return render(request, 'core/add_question_to_test.html', {'form': form, 'test': test})

@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('view_test', test_id=question.test.test_id)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'core/edit_question.html', {'form': form, 'question': question})

@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    test_id = question.test.test_id
    question.delete()
    return redirect('view_test', test_id=test_id)

@login_required
def view_test_student(request, test_id):
    test = Test.objects.get(pk=test_id)
    questions = test.question_set.all()

    if request.method == 'POST':
        form = TestSubmissionForm(request.POST)
        if form.is_valid():
            student = request.user
            for question in questions:
                answer_text = form.cleaned_data.get(f'question_answer_{question.pk}')
                submission = Submission.objects.create(
                    question_answer=answer_text,
                    student=student,
                    question=question
                )
            return redirect('student_dashboard')
    else:
        form = TestSubmissionForm()

    context = {
        'form': form,
        'test': test,
        'questions': questions,
    }
    return render(request, 'core/view_test_student.html', context)