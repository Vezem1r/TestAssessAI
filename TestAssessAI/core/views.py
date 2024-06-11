from django.db.models import Sum
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Subject, Test, Question, Submission, Mark
from user.models import User, Student
from django.contrib.auth import get_user_model
from .forms import QuestionForm, TestForm, TestSubmissionForm
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponseBadRequest
from dataclasses import dataclass

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
        Subject.objects.create(
            lesson_title=title, description=description, teacher=request.user)
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
            subject_url = reverse('view_subject', kwargs={
                                  'subject_id': subject_id})
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
        subject_test_list = []
        for test in tests:
            questions = test.question_set.all()
            num_questions = questions.count()
            submissions = Submission.objects.filter(
                student=request.user, question__in=questions)
            question_scores = []
            for submission in submissions:
                mark = Mark.objects.filter(submission=submission).first()
                if mark:
                    question_scores.append(mark.teacher_mark)
                else:
                    question_scores.append(0)
            
            question_scores = question_scores[-num_questions:]
            total_score = sum(question_scores)
            subject_test_list.append({
                'test': test,
                'question_scores': question_scores,
                'total_score': total_score
            })

        subject_tests.append({
            'subject': subject,
            'tests': subject_test_list
        })

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
    total_score = sum(question.score for question in test.question_set.all())
    return render(request, 'core/view_test.html', {'test': test, 'total_score': total_score})

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
    if request.method == 'POST' and request.user.is_teacher():
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

@dataclass
class FormQuestion:
    question_id: int
    question_anwser: str

@login_required
def view_test_student(request, test_id):
    test = Test.objects.get(pk=test_id)
    questions = test.question_set.all()
    form_questions = []

    if request.method == 'POST' and request.user.is_student():
        form_questions = [FormQuestion(question_id=int(key.split('question_answer_')[1]), question_anwser=value) for key,
                          value in request.POST.items() if 'question_answer' in key]

        for form_question in form_questions:
            student = request.user
            question = next(
                (question for question in questions if question.pk == form_question.question_id), None)
            submission = Submission.objects.create(
                question_answer=form_question.question_anwser,
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

@login_required
def review_submission(request, test_id, student_id):
    test = get_object_or_404(Test, pk=test_id)
    student = get_object_or_404(Student, pk=student_id)
    questions = Question.objects.filter(test=test)
    submissions = Submission.objects.filter(student=student, question__in=questions)

    questions_with_submissions = []
    for question in questions:
        submission = next((sub for sub in reversed(submissions) if sub.question.question_id == question.question_id), None)
        mark = Mark.objects.filter(submission=submission).first() if submission else None
        teacher_mark = mark.teacher_mark if mark else None
        print("Question ID:", question.pk, "Submission ID:", submission.pk if submission else None, "Teacher Mark:", teacher_mark)
        questions_with_submissions.append({
            'question': question,
            'submission': submission,
            'teacher_mark': teacher_mark
        })

    context = {
        'test': test,
        'student': student,
        'questions_with_submissions': questions_with_submissions
    }
    return render(request, 'core/review_submission.html', context)

@login_required
def view_student_tests(request, student_id, subject_id):
    student = get_object_or_404(Student, pk=student_id)
    subject = get_object_or_404(Subject, pk=subject_id)
    tests = Test.objects.filter(subject=subject, subject__students=student).distinct()

    tests_with_scores = []
    for test in tests:
        num_questions = Question.objects.filter(test=test).count()
        submissions = Submission.objects.filter(student=student, question__test=test).order_by('-submission_id')
        latest_marks = Mark.objects.filter(submission__in=submissions[:num_questions]).values_list('teacher_mark', flat=True)
        total_score = sum(latest_marks) if latest_marks else "N/A"
        
        tests_with_scores.append({
            'test': test,
            'total_score': total_score
        })

    return render(request, 'core/view_student_tests.html', {'student': student, 'subject': subject, 'tests_with_scores': tests_with_scores})

@login_required
def review_submission_teacher(request, test_id, student_id):
    test = get_object_or_404(Test, pk=test_id)
    student = get_object_or_404(Student, pk=student_id)
    questions = Question.objects.filter(test=test)
    submissions = Submission.objects.filter(student=student, question__in=questions).order_by('-submission_id')
    subject_id = test.subject.subject_id
    if request.method == 'POST' and request.user.is_teacher():
        for question in questions:
            mark_value = request.POST.get('mark_' + str(question.pk))
            submission = submissions.filter(question=question).first()
            if submission and mark_value is not None:
                try:
                    mark_value = float(mark_value)
                    if 0 <= mark_value <= question.score:
                        
                        mark, created = Mark.objects.get_or_create(
                            submission=submission, 
                            teacher=request.user, 
                            defaults={'ai_mark': 0, 'teacher_mark': mark_value}
                        )
                        if not created:
                            mark.teacher_mark = mark_value
                        mark.save()
                    else:
                        return HttpResponseBadRequest("Invalid mark value for question: " + question.question_text)
                except ValueError:
                    return HttpResponseBadRequest("Invalid mark value for question: " + question.question_text)
        return redirect('view_student_tests', subject_id = subject_id,  student_id=student_id)

    context = {
        'test': test,
        'student': student,
        'questions_with_submissions': [{'question': q, 'submission': submissions.filter(question=q).first()} for q in questions]
    }
    return render(request, 'core/review_submission_teacher.html', context)

def save_review(request, test_id, student_id):
    test = get_object_or_404(Test, pk=test_id)
    student = get_object_or_404(Student, pk=student_id)
    questions = Question.objects.filter(test=test)
    submissions = Submission.objects.filter(student=student, question__in=questions)

    if request.method == 'POST' and request.user.is_teacher():
        for question in questions:
            mark_value = request.POST.get('mark_' + str(question.pk))
            submission = submissions.filter(question=question).first()
            if submission and mark_value is not None:
                try:
                    mark_value = float(mark_value)
                    if 0 <= mark_value <= question.score:
                        
                        mark, created = Mark.objects.get_or_create(
                            submission=submission, 
                            teacher=request.user, 
                            defaults={'ai_mark': 0, 'teacher_mark': mark_value}
                        )
                        if not created:
                            mark.teacher_mark = mark_value
                        mark.save()
                    else:
                        return HttpResponseBadRequest("Invalid mark value for question: " + question.question_text)
                except ValueError:
                    return HttpResponseBadRequest("Invalid mark value for question: " + question.question_text)
        return redirect('teacher_dashboard')

    context = {
        'test': test,
        'student': student,
        'questions_with_submissions': [{'question': q, 'submission': submissions.filter(question=q).first()} for q in questions]
    }
    return render(request, 'core/review_submission_teacher.html', context)

