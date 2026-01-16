from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db.models import Avg, Count, Sum, Q
from .models import (
    User, Student, Exam, Question, ExamAttempt, StudentAnswer,
    Category, Notification, Achievement, StudentAchievement
)
from .serializers import (
    UserSerializer, RegisterSerializer, StudentSerializer, StudentProfileSerializer,
    ExamSerializer, ExamWithQuestionsSerializer, QuestionSerializer,
    ExamAttemptSerializer, ExamAttemptDetailSerializer, ExamSubmitSerializer, 
    ResultSerializer, CategorySerializer, NotificationSerializer,
    AchievementSerializer, StudentAchievementSerializer, LeaderboardSerializer,
    AnalyticsSerializer
)
import random

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access_token': str(refresh.access_token),
            'token_type': 'bearer',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    try:
        user = User.objects.get(email=email)
        user = authenticate(username=user.username, password=password)
    except User.DoesNotExist:
        user = None
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'token_type': 'bearer',
            'user': UserSerializer(user).data
        })
    
    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.filter(is_active=True)
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        exam_type = self.request.query_params.get('type', None)
        category = self.request.query_params.get('category', None)
        
        if exam_type:
            queryset = queryset.filter(exam_type=exam_type)
        if category:
            queryset = queryset.filter(category_id=category)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ExamWithQuestionsSerializer
        return ExamSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]
    
    def retrieve(self, request, *args, **kwargs):
        exam = self.get_object()
        
        # Check if exam is scheduled and accessible
        if exam.start_date and exam.end_date:
            if not exam.is_scheduled():
                if exam.is_upcoming():
                    return Response({'detail': 'Exam has not started yet'}, status=status.HTTP_403_FORBIDDEN)
                if exam.is_expired():
                    return Response({'detail': 'Exam has expired'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(exam)
        data = serializer.data
        
        # Shuffle questions if enabled
        if exam.shuffle_questions and 'questions' in data:
            random.shuffle(data['questions'])
        
        return Response(data)
    
    def destroy(self, request, *args, **kwargs):
        exam = self.get_object()
        exam.is_active = False
        exam.save()
        return Response({'message': 'Exam deleted successfully'})
    
    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming(self, request):
        now = timezone.now()
        exams = Exam.objects.filter(is_active=True, start_date__gt=now)
        serializer = self.get_serializer(exams, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='active')
    def active(self, request):
        now = timezone.now()
        exams = Exam.objects.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        )
        serializer = self.get_serializer(exams, many=True)
        return Response(serializer.data)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdmin]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        exam_id = self.request.query_params.get('exam', None)
        category = self.request.query_params.get('category', None)
        difficulty = self.request.query_params.get('difficulty', None)
        
        if exam_id:
            queryset = queryset.filter(exam_id=exam_id)
        if category:
            queryset = queryset.filter(category_id=category)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        return queryset
    
    @action(detail=False, methods=['get'], url_path='exam/(?P<exam_id>[^/.]+)')
    def by_exam(self, request, exam_id=None):
        questions = Question.objects.filter(exam_id=exam_id)
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='bank')
    def question_bank(self, request):
        # Questions not assigned to any exam
        questions = Question.objects.filter(exam__isnull=True)
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)

class StudentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            student = Student.objects.get(user=request.user)
            serializer = StudentProfileSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({'detail': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({'detail': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='start-exam')
    def start_exam(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({'detail': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        exam_id = request.data.get('exam_id')
        exam = Exam.objects.get(id=exam_id)
        
        # Check max attempts
        if exam.max_attempts > 0:
            attempts_count = ExamAttempt.objects.filter(student=student, exam=exam).count()
            if attempts_count >= exam.max_attempts:
                return Response({'detail': f'Maximum {exam.max_attempts} attempts allowed'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get attempt number
        attempt_number = ExamAttempt.objects.filter(student=student, exam=exam).count() + 1
        
        attempt = ExamAttempt.objects.create(
            student=student,
            exam=exam,
            attempt_number=attempt_number,
            status='in_progress'
        )
        
        serializer = ExamAttemptSerializer(attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], url_path='pause-exam')
    def pause_exam(self, request):
        attempt_id = request.data.get('attempt_id')
        try:
            attempt = ExamAttempt.objects.get(id=attempt_id)
            attempt.status = 'paused'
            attempt.pause_time = timezone.now()
            attempt.save()
            return Response({'message': 'Exam paused successfully'})
        except ExamAttempt.DoesNotExist:
            return Response({'detail': 'Exam attempt not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'], url_path='resume-exam')
    def resume_exam(self, request):
        attempt_id = request.data.get('attempt_id')
        try:
            attempt = ExamAttempt.objects.get(id=attempt_id)
            attempt.status = 'in_progress'
            attempt.resume_time = timezone.now()
            attempt.save()
            return Response({'message': 'Exam resumed successfully'})
        except ExamAttempt.DoesNotExist:
            return Response({'detail': 'Exam attempt not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'], url_path='submit-exam')
    def submit_exam(self, request):
        serializer = ExamSubmitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        attempt_id = serializer.validated_data['attempt_id']
        answers = serializer.validated_data['answers']
        
        try:
            attempt = ExamAttempt.objects.get(id=attempt_id)
        except ExamAttempt.DoesNotExist:
            return Response({'detail': 'Exam attempt not found'}, status=status.HTTP_404_NOT_FOUND)
        
        exam = attempt.exam
        correct_count = 0
        wrong_count = 0
        total_score = 0
        
        # Get all questions for this exam
        all_questions = exam.questions.all()
        answered_question_ids = [ans['question_id'] for ans in answers]
        
        for answer_data in answers:
            question = Question.objects.get(id=answer_data['question_id'])
            selected = answer_data['selected_answer']
            time_taken = answer_data.get('time_taken', 0)
            
            is_correct = question.correct_answer == selected
            marks_obtained = 0
            
            if is_correct:
                correct_count += 1
                marks_obtained = question.marks
                total_score += question.marks
            else:
                wrong_count += 1
                # Apply negative marking if enabled
                if exam.negative_marking:
                    marks_obtained = -exam.negative_marks
                    total_score -= exam.negative_marks
            
            StudentAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_answer=selected,
                is_correct=is_correct,
                time_taken=time_taken,
                marks_obtained=marks_obtained
            )
        
        # Calculate unanswered questions
        unanswered = all_questions.count() - len(answers)
        
        # Calculate time spent
        time_spent = (timezone.now() - attempt.start_time).total_seconds()
        
        # Calculate percentage
        percentage = (total_score / exam.total_marks) * 100 if exam.total_marks > 0 else 0
        
        attempt.end_time = timezone.now()
        attempt.score = total_score
        attempt.percentage = percentage
        attempt.total_questions = all_questions.count()
        attempt.correct_answers = correct_count
        attempt.wrong_answers = wrong_count
        attempt.unanswered = unanswered
        attempt.time_spent = int(time_spent)
        attempt.status = 'completed'
        attempt.save()
        
        # Update student points
        student = attempt.student
        student.total_points += int(total_score)
        student.save()
        
        # Calculate rank for this exam
        calculate_exam_ranks(exam.id)
        
        # Update global ranks
        update_global_ranks()
        
        # Check and award achievements
        check_achievements(student)
        
        # Send notification
        Notification.objects.create(
            user=student.user,
            notification_type='result_published',
            title='Exam Completed',
            message=f'You scored {total_score}/{exam.total_marks} ({percentage:.2f}%) in {exam.title}'
        )
        
        return Response({
            'message': 'Exam submitted successfully',
            'score': total_score,
            'percentage': percentage,
            'correct_answers': correct_count,
            'wrong_answers': wrong_count,
            'unanswered': unanswered,
            'total_questions': all_questions.count(),
            'rank': attempt.rank
        })
    
    @action(detail=False, methods=['get'], url_path='my-attempts')
    def my_attempts(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({'detail': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        attempts = ExamAttempt.objects.filter(student=student)
        serializer = ExamAttemptSerializer(attempts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='analytics')
    def analytics(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({'detail': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        attempts = ExamAttempt.objects.filter(student=student, status='completed')
        
        total_exams = Exam.objects.filter(is_active=True).count()
        completed_exams = attempts.count()
        
        avg_score = attempts.aggregate(Avg('percentage'))['percentage__avg'] or 0
        highest_score = attempts.aggregate(Max('percentage'))['percentage__max'] or 0
        total_time = attempts.aggregate(Sum('time_spent'))['time_spent__sum'] or 0
        
        # Category-wise performance
        category_performance = {}
        for attempt in attempts:
            if attempt.exam.category:
                cat_name = attempt.exam.category.name
                if cat_name not in category_performance:
                    category_performance[cat_name] = {'total': 0, 'sum': 0}
                category_performance[cat_name]['total'] += 1
                category_performance[cat_name]['sum'] += attempt.percentage
        
        for cat in category_performance:
            category_performance[cat] = category_performance[cat]['sum'] / category_performance[cat]['total']
        
        # Difficulty-wise performance
        difficulty_performance = {'easy': 0, 'medium': 0, 'hard': 0}
        
        analytics_data = {
            'total_exams': total_exams,
            'completed_exams': completed_exams,
            'average_score': round(avg_score, 2),
            'highest_score': round(highest_score, 2),
            'total_time_spent': total_time,
            'category_wise_performance': category_performance,
            'difficulty_wise_performance': difficulty_performance,
            'recent_attempts': ExamAttemptSerializer(attempts[:5], many=True).data
        }
        
        serializer = AnalyticsSerializer(analytics_data)
        return Response(serializer.data)

class ResultViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'], url_path='attempt/(?P<attempt_id>[^/.]+)')
    def by_attempt(self, request, attempt_id=None):
        try:
            attempt = ExamAttempt.objects.get(id=attempt_id)
        except ExamAttempt.DoesNotExist:
            return Response({'detail': 'Exam attempt not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user.role == 'student':
            try:
                student = Student.objects.get(user=request.user)
                if student.id != attempt.student.id:
                    return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
            except Student.DoesNotExist:
                return Response({'detail': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        result_status = 'Pass' if attempt.score >= attempt.exam.passing_marks else 'Fail'
        
        result = {
            'attempt_id': attempt.id,
            'exam_title': attempt.exam.title,
            'student_name': attempt.student.name,
            'score': attempt.score,
            'total_marks': attempt.exam.total_marks,
            'percentage': attempt.percentage,
            'correct_answers': attempt.correct_answers,
            'wrong_answers': attempt.wrong_answers,
            'unanswered': attempt.unanswered,
            'rank': attempt.rank,
            'status': result_status,
            'start_time': attempt.start_time,
            'end_time': attempt.end_time,
            'time_spent': attempt.time_spent
        }
        
        serializer = ResultSerializer(result)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='attempt/(?P<attempt_id>[^/.]+)/detailed')
    def detailed_result(self, request, attempt_id=None):
        try:
            attempt = ExamAttempt.objects.get(id=attempt_id)
        except ExamAttempt.DoesNotExist:
            return Response({'detail': 'Exam attempt not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Only show detailed results if exam allows or user is admin
        if not attempt.exam.show_results_immediately and request.user.role != 'admin':
            return Response({'detail': 'Detailed results not available yet'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ExamAttemptDetailSerializer(attempt)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='exam/(?P<exam_id>[^/.]+)', permission_classes=[IsAdmin])
    def by_exam(self, request, exam_id=None):
        attempts = ExamAttempt.objects.filter(exam_id=exam_id, status='completed')
        exam = Exam.objects.get(id=exam_id)
        
        results = []
        for attempt in attempts:
            result_status = 'Pass' if attempt.score >= exam.passing_marks else 'Fail'
            
            results.append({
                'attempt_id': attempt.id,
                'exam_title': exam.title,
                'student_name': attempt.student.name,
                'score': attempt.score,
                'total_marks': exam.total_marks,
                'percentage': attempt.percentage,
                'correct_answers': attempt.correct_answers,
                'wrong_answers': attempt.wrong_answers,
                'unanswered': attempt.unanswered,
                'rank': attempt.rank,
                'status': result_status,
                'start_time': attempt.start_time,
                'end_time': attempt.end_time,
                'time_spent': attempt.time_spent
            })
        
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)

class LeaderboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def global_leaderboard(self, request):
        students = Student.objects.all().order_by('-total_points')[:50]
        
        leaderboard_data = []
        for idx, student in enumerate(students, 1):
            completed = ExamAttempt.objects.filter(student=student, status='completed').count()
            avg_score = ExamAttempt.objects.filter(student=student, status='completed').aggregate(Avg('percentage'))['percentage__avg'] or 0
            
            leaderboard_data.append({
                'rank': idx,
                'student_name': student.name,
                'total_points': student.total_points,
                'exams_completed': completed,
                'average_score': round(avg_score, 2),
                'profile_image': student.profile_image.url if student.profile_image else None
            })
        
        serializer = LeaderboardSerializer(leaderboard_data, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='exam/(?P<exam_id>[^/.]+)')
    def exam_leaderboard(self, request, exam_id=None):
        attempts = ExamAttempt.objects.filter(
            exam_id=exam_id, 
            status='completed'
        ).order_by('-score', 'time_spent')[:50]
        
        leaderboard_data = []
        for idx, attempt in enumerate(attempts, 1):
            leaderboard_data.append({
                'rank': idx,
                'student_name': attempt.student.name,
                'total_points': int(attempt.score),
                'exams_completed': 1,
                'average_score': attempt.percentage,
                'profile_image': attempt.student.profile_image.url if attempt.student.profile_image else None
            })
        
        serializer = LeaderboardSerializer(leaderboard_data, many=True)
        return Response(serializer.data)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'], url_path='mark-read')
    def mark_read(self, request):
        notification_ids = request.data.get('notification_ids', [])
        Notification.objects.filter(id__in=notification_ids, user=request.user).update(is_read=True)
        return Response({'message': 'Notifications marked as read'})
    
    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'message': 'All notifications marked as read'})

class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'], url_path='my-achievements')
    def my_achievements(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({'detail': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        achievements = StudentAchievement.objects.filter(student=student)
        serializer = StudentAchievementSerializer(achievements, many=True)
        return Response(serializer.data)

# Helper functions
def calculate_exam_ranks(exam_id):
    attempts = ExamAttempt.objects.filter(
        exam_id=exam_id,
        status='completed'
    ).order_by('-score', 'time_spent')
    
    for idx, attempt in enumerate(attempts, 1):
        attempt.rank = idx
        attempt.save(update_fields=['rank'])

def update_global_ranks():
    students = Student.objects.all().order_by('-total_points')
    for idx, student in enumerate(students, 1):
        student.rank = idx
        student.save(update_fields=['rank'])

def check_achievements(student):
    completed_exams = ExamAttempt.objects.filter(student=student, status='completed').count()
    
    # Check for achievements
    achievements_to_award = []
    
    # First exam completed
    if completed_exams == 1:
        try:
            achievement = Achievement.objects.get(criteria='complete_first_exam')
            StudentAchievement.objects.get_or_create(student=student, achievement=achievement)
        except Achievement.DoesNotExist:
            pass
    
    # 10 exams completed
    if completed_exams == 10:
        try:
            achievement = Achievement.objects.get(criteria='complete_10_exams')
            StudentAchievement.objects.get_or_create(student=student, achievement=achievement)
        except Achievement.DoesNotExist:
            pass
    
    # Perfect score
    perfect_scores = ExamAttempt.objects.filter(student=student, percentage=100).count()
    if perfect_scores >= 1:
        try:
            achievement = Achievement.objects.get(criteria='score_100_percent')
            StudentAchievement.objects.get_or_create(student=student, achievement=achievement)
        except Achievement.DoesNotExist:
            pass
