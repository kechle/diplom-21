from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Course, Lesson, Test, UserProgress

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 9

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_progress'] = UserProgress.objects.filter(
                user=self.request.user,
                lesson__course=self.object
            )
        return context

@login_required
def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.user not in course.students.all():
        course.students.add(request.user)
        messages.success(request, f'Вы успешно записались на курс "{course.title}"')
    return redirect('courses:course_detail', slug=slug)

@login_required
def lesson_detail(request, course_slug, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, course__slug=course_slug)
    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )
    
    if request.method == 'POST':
        progress.completed = True
        progress.save()
        messages.success(request, 'Урок отмечен как пройденный!')
        return redirect('courses:course_detail', slug=course_slug)
    
    return render(request, 'courses/lesson_detail.html', {
        'lesson': lesson,
        'progress': progress
    })
