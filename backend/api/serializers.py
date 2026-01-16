from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student, Exam, Question, ExamAttempt, StudentAnswer

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
    class Meta:
        model = Student
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class QuestionForStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'marks', 'image')

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

class ExamWithQuestionsSerializer(serializers.ModelSerializer):
    questions = QuestionForStudentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Exam
        fields = '__all__'

class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = ('question_id', 'selected_answer')

class ExamSubmitSerializer(serializers.Serializer):
    attempt_id = serializers.IntegerField()
    answers = StudentAnswerSerializer(many=True)

class ExamAttemptSerializer(serializers.ModelSerializer):
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
    status = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
