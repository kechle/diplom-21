from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserUpdateForm
from .models import User
from courses.forms import CourseForm, LessonForm
from .forms import AddStudentToCourseForm
from courses.models import Course, Lesson, UserCourse
from django.db import IntegrityError

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    user_courses = UserCourse.objects.filter(user=request.user).select_related('course')
    context = {
        'user': request.user,
        'user_courses': user_courses
    }
    return render(request, 'users/profile.html', context)

@login_required
def dashboard(request):
    user = request.user
    if user.is_admin:
        return redirect('admin_dashboard')
    elif user.is_teacher:
        return redirect('teacher_dashboard')
    elif user.is_student:
        return redirect('student_dashboard')
    else:
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('home')

@login_required
def admin_dashboard(request):
    if not (request.user.is_admin or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('home')

    course_form = CourseForm(request.POST or None, request.FILES or None)
    lesson_form = LessonForm(request.POST or None)
    add_student_form = AddStudentToCourseForm(request.POST or None)

    if request.method == 'POST':
        if 'add_course' in request.POST and course_form.is_valid():
            try:
                course_form.save()
                messages.success(request, 'Курс успешно добавлен!')
                return redirect('users:admin_dashboard')
            except IntegrityError:
                messages.error(request, 'Курс с таким названием уже существует!')
        if 'add_lesson' in request.POST and lesson_form.is_valid():
            lesson_form.save()
            messages.success(request, 'Лекция успешно добавлена!')
            return redirect('users:admin_dashboard')
        if 'add_student' in request.POST and add_student_form.is_valid():
            course = add_student_form.cleaned_data['course']
            student = add_student_form.cleaned_data['student']
            course.students.add(student)
            messages.success(request, f'Студент {student.username} добавлен к курсу {course.title}!')
            return redirect('users:admin_dashboard')

    courses = Course.objects.all()
    lessons = Lesson.objects.all()

    return render(request, 'users/admin_dashboard.html', {
        'course_form': course_form,
        'lesson_form': lesson_form,
        'add_student_form': add_student_form,
        'courses': courses,
        'lessons': lessons,
    })

def logout_view(request):
    logout(request)
    return redirect('home')
