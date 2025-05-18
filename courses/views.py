from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Course, Lesson, Test, UserProgress, Question, UserCourse

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
    questions = lesson.questions.all()
    user_progress = UserProgress.objects.filter(user=request.user, lesson__course=lesson.course)
    test_result = None
    percentage = None
    if request.method == 'POST' and questions.exists():
        score = 0
        total_questions = questions.count()
        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}')
            if user_answer == question.correct_answer:
                score += 1
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        test_result = {
            'score': score,
            'total_questions': total_questions,
            'percentage': percentage,
        }
        if score == total_questions and total_questions > 0:
            progress.completed = True
            progress.save()
            messages.success(request, 'Урок отмечен как пройденный!')
        else:
            progress.completed = False
            progress.save()
            messages.error(request, f'Тест не пройден. Правильных ответов: {score} из {total_questions}')
    return render(request, 'courses/lesson_detail.html', {
        'lesson': lesson,
        'progress': progress,
        'questions': questions,
        'user_progress': user_progress,
        'test_result': test_result,
        'percentage': percentage,
    })

def home(request):
    popular_courses = Course.objects.filter(is_popular=True)[:6]
    context = {
        'popular_courses': popular_courses
    }
    return render(request, 'home.html', context)

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = UserCourse.objects.filter(user=request.user, course=course).exists()
    
    context = {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled
    }
    return render(request, 'courses/course_detail.html', context)
