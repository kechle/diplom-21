from django.contrib import admin
from .models import Course, Lesson, Test, Question, Answer, UserProgress

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'created_at', 'updated_at', 'get_students_count')
    list_filter = ('created_at', 'updated_at', 'teacher')
    search_fields = ('title', 'description', 'teacher__username')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('students',)

    def get_students_count(self, obj):
        return obj.students.count()
    get_students_count.short_description = 'Количество студентов'

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'content', 'course__title')
    ordering = ('course', 'order')

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'created_at')
    list_filter = ('lesson__course', 'created_at')
    search_fields = ('title', 'description', 'lesson__title')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test', 'order')
    list_filter = ('test__lesson__course', 'test')
    search_fields = ('text', 'test__title')
    ordering = ('test', 'order')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('question__test__lesson__course', 'is_correct')
    search_fields = ('text', 'question__text')

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'completed_at')
    list_filter = ('completed', 'completed_at', 'lesson__course')
    search_fields = ('user__username', 'lesson__title')
    readonly_fields = ('completed_at',)
