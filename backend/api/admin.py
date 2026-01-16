from django.contrib import admin
from .models import User, Student, Exam, Question, ExamAttempt, StudentAnswer, Category, Notification, Achievement, StudentAchievement

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'enrollment_no', 'total_points', 'rank', 'created_at')
    search_fields = ('name', 'email', 'enrollment_no')
    list_filter = ('created_at',)
    readonly_fields = ('total_points', 'rank')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'exam_type', 'duration', 'total_marks', 'passing_marks', 'is_active', 'start_date', 'end_date')
    list_filter = ('is_active', 'exam_type', 'category', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('get_question_preview', 'exam', 'category', 'question_type', 'difficulty', 'correct_answer', 'marks')
    list_filter = ('exam', 'category', 'question_type', 'difficulty')
    search_fields = ('question_text',)
    
    def get_question_preview(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
    get_question_preview.short_description = 'Question'

@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'attempt_number', 'score', 'percentage', 'status', 'rank', 'start_time')
    list_filter = ('status', 'exam')
    search_fields = ('student__name', 'exam__title')
    readonly_fields = ('start_time', 'time_spent')

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_answer', 'is_correct', 'marks_obtained', 'time_taken')
    list_filter = ('is_correct',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'points', 'criteria')
    search_fields = ('name', 'criteria')

@admin.register(StudentAchievement)
class StudentAchievementAdmin(admin.ModelAdmin):
    list_display = ('student', 'achievement', 'earned_at')
    list_filter = ('achievement', 'earned_at')
    search_fields = ('student__name', 'achievement__name')
