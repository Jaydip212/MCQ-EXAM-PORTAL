from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    register, login, ExamViewSet, QuestionViewSet,
    StudentViewSet, ResultViewSet, CategoryViewSet,
    LeaderboardViewSet, NotificationViewSet, AchievementViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'results', ResultViewSet, basename='result')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'achievements', AchievementViewSet, basename='achievement')

urlpatterns = [
    path('auth/register', register, name='register'),
    path('auth/login', login, name='login'),
    path('', include(router.urls)),
]
