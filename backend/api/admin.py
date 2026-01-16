from django.contrib import admin
from .models import User, Student, Exam, Question, ExamAttempt, StudentAnswer

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'enrollment_no', 'created_at')
    search_fields = ('name', 'email', 'enrollment_no')

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'total_marks', 'passing_marks', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'question_text', 'correct_answer', 'marks')
    list_filter = ('exam',)
    search_fields = ('question_text',)

@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'score', 'status', 'start_time')
    list_filter = ('status', 'exam')
    search_fields = ('student__name', 'exam__title')

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_answer', 'is_correct')
    list_filter = ('is_correct',)
