from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    register, login, ExamViewSet, QuestionViewSet,
    StudentViewSet, ResultViewSet
)

router = DefaultRouter()
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'results', ResultViewSet, basename='result')

urlpatterns = [
    path('auth/register', register, name='register'),
    path('auth/login', login, name='login'),
    path('', include(router.urls)),
]
