from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User, Student, Exam, Question, ExamAttempt, StudentAnswer
from .serializers import (
    UserSerializer, RegisterSerializer, StudentSerializer,
    ExamSerializer, ExamWithQuestionsSerializer, QuestionSerializer,
    ExamAttemptSerializer, ExamSubmitSerializer, ResultSerializer
)

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

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.filter(is_active=True)
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ExamWithQuestionsSerializer
        return ExamSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]
    
    def destroy(self, request, *args, **kwargs):
        exam = self.get_object()
        exam.is_active = False
        exam.save()
        return Response({'message': 'Exam deleted successfully'})

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdmin]
    
    @action(detail=False, methods=['get'], url_path='exam/(?P<exam_id>[^/.]+)')
    def by_exam(self, request, exam_id=None):
        questions = Question.objects.filter(exam_id=exam_id)
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)

class StudentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            student = Student.objects.get(user=request.user)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({'detail': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'], url_path='start-exam')
    def start_exam(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({'detail': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        exam_id = request.data.get('exam_id')
        exam = Exam.objects.get(id=exam_id)
        
        attempt = ExamAttempt.objects.create(
            student=student,
            exam=exam,
            status='in_progress'
        )
        
        serializer = ExamAttemptSerializer(attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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
        
        correct_count = 0
        total_score = 0
        
        for answer_data in answers:
            question = Question.objects.get(id=answer_data['question_id'])
            selected = answer_data['selected_answer']
            is_correct = question.correct_answer == selected
            
            if is_correct:
                correct_count += 1
                total_score += question.marks
            
            StudentAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_answer=selected,
                is_correct=is_correct
            )
        
        attempt.end_time = timezone.now()
        attempt.score = total_score
        attempt.total_questions = len(answers)
        attempt.correct_answers = correct_count
        attempt.status = 'completed'
        attempt.save()
        
        return Response({
            'message': 'Exam submitted successfully',
            'score': total_score,
            'correct_answers': correct_count,
            'total_questions': len(answers)
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
        
        percentage = (attempt.score / attempt.exam.total_marks) * 100 if attempt.exam.total_marks > 0 else 0
        result_status = 'Pass' if attempt.score >= attempt.exam.passing_marks else 'Fail'
        
        result = {
            'attempt_id': attempt.id,
            'exam_title': attempt.exam.title,
            'student_name': attempt.student.name,
            'score': attempt.score,
            'total_marks': attempt.exam.total_marks,
            'percentage': percentage,
            'status': result_status,
            'start_time': attempt.start_time,
            'end_time': attempt.end_time
        }
        
        serializer = ResultSerializer(result)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='exam/(?P<exam_id>[^/.]+)', permission_classes=[IsAdmin])
    def by_exam(self, request, exam_id=None):
        attempts = ExamAttempt.objects.filter(exam_id=exam_id, status='completed')
        exam = Exam.objects.get(id=exam_id)
        
        results = []
        for attempt in attempts:
            percentage = (attempt.score / exam.total_marks) * 100 if exam.total_marks > 0 else 0
            result_status = 'Pass' if attempt.score >= exam.passing_marks else 'Fail'
            
            results.append({
                'attempt_id': attempt.id,
                'exam_title': exam.title,
                'student_name': attempt.student.name,
                'score': attempt.score,
                'total_marks': exam.total_marks,
                'percentage': percentage,
                'status': result_status,
                'start_time': attempt.start_time,
                'end_time': attempt.end_time
            })
        
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)
