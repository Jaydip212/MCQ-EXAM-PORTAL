from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student, Exam, Question, ExamAttempt, StudentAnswer, Category, Notification, Achievement, StudentAchievement

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'student')
        )
        
        if user.role == 'student':
            Student.objects.create(
                user=user,
                name=user.username,
                email=user.email
            )
        
        return user

class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    achievements_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ('id', 'username', 'name', 'email', 'phone', 'enrollment_no', 'profile_image', 'bio', 'total_points', 'rank', 'achievements_count', 'created_at')
    
    def get_achievements_count(self, obj):
        return obj.achievements.count()

class CategorySerializer(serializers.ModelSerializer):
    exams_count = serializers.SerializerMethodField()
    questions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = '__all__'
    
    def get_exams_count(self, obj):
        return obj.exams.count()
    
    def get_questions_count(self, obj):
        return obj.questions.count()

class QuestionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Question
        fields = '__all__'

class QuestionForStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question_type', 'difficulty', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'marks', 'image')

class ExamSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    questions_count = serializers.SerializerMethodField()
    is_scheduled_now = serializers.SerializerMethodField()
    is_upcoming_exam = serializers.SerializerMethodField()
    is_expired_exam = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = '__all__'
    
    def get_questions_count(self, obj):
        return obj.questions.count()
    
    def get_is_scheduled_now(self, obj):
        return obj.is_scheduled()
    
    def get_is_upcoming_exam(self, obj):
        return obj.is_upcoming()
    
    def get_is_expired_exam(self, obj):
        return obj.is_expired()

class ExamWithQuestionsSerializer(serializers.ModelSerializer):
    questions = QuestionForStudentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Exam
        fields = '__all__'

class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = ('question_id', 'selected_answer', 'time_taken')

class StudentAnswerDetailSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.question_text', read_only=True)
    correct_answer = serializers.CharField(source='question.correct_answer', read_only=True)
    explanation = serializers.CharField(source='question.explanation', read_only=True)
    
    class Meta:
        model = StudentAnswer
        fields = '__all__'

class ExamSubmitSerializer(serializers.Serializer):
    attempt_id = serializers.IntegerField()
    answers = StudentAnswerSerializer(many=True)

class ExamAttemptSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    
    class Meta:
        model = ExamAttempt
        fields = '__all__'

class ExamAttemptDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    answers = StudentAnswerDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = ExamAttempt
        fields = '__all__'

class ResultSerializer(serializers.Serializer):
    attempt_id = serializers.IntegerField()
    exam_title = serializers.CharField()
    student_name = serializers.CharField()
    score = serializers.FloatField()
    total_marks = serializers.IntegerField()
    percentage = serializers.FloatField()
    correct_answers = serializers.IntegerField()
    wrong_answers = serializers.IntegerField()
    unanswered = serializers.IntegerField()
    rank = serializers.IntegerField(allow_null=True)
    status = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    time_spent = serializers.IntegerField()

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'

class StudentAchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source='achievement.name', read_only=True)
    achievement_icon = serializers.CharField(source='achievement.icon', read_only=True)
    achievement_points = serializers.IntegerField(source='achievement.points', read_only=True)
    
    class Meta:
        model = StudentAchievement
        fields = '__all__'

class LeaderboardSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    student_name = serializers.CharField()
    total_points = serializers.IntegerField()
    exams_completed = serializers.IntegerField()
    average_score = serializers.FloatField()
    profile_image = serializers.ImageField(allow_null=True)

class AnalyticsSerializer(serializers.Serializer):
    total_exams = serializers.IntegerField()
    completed_exams = serializers.IntegerField()
    average_score = serializers.FloatField()
    highest_score = serializers.FloatField()
    total_time_spent = serializers.IntegerField()
    category_wise_performance = serializers.DictField()
    difficulty_wise_performance = serializers.DictField()
    recent_attempts = ExamAttemptSerializer(many=True)
