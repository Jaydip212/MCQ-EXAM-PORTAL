from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    
    def __str__(self):
        return self.username

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    enrollment_no = models.CharField(max_length=50, unique=True, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    total_points = models.IntegerField(default=0)
    rank = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Exam(models.Model):
    EXAM_TYPE_CHOICES = (
        ('practice', 'Practice'),
        ('mock', 'Mock Test'),
        ('final', 'Final Exam'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='exams')
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES, default='final')
    duration = models.IntegerField(help_text='Duration in minutes')
    total_marks = models.IntegerField()
    passing_marks = models.IntegerField()
    negative_marking = models.BooleanField(default=False)
    negative_marks = models.FloatField(default=0.0, help_text='Marks to deduct for wrong answer')
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    max_attempts = models.IntegerField(default=1, help_text='Max attempts allowed (0 for unlimited in practice mode)')
    show_results_immediately = models.BooleanField(default=False)
    shuffle_questions = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_scheduled(self):
        if not self.start_date or not self.end_date:
            return False
        now = timezone.now()
        return self.start_date <= now <= self.end_date
    
    def is_upcoming(self):
        if not self.start_date:
            return False
        return timezone.now() < self.start_date
    
    def is_expired(self):
        if not self.end_date:
            return False
        return timezone.now() > self.end_date
    
    def __str__(self):
        return self.title

class Question(models.Model):
    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    
    QUESTION_TYPE_CHOICES = (
        ('single', 'Single Choice'),
        ('multiple', 'Multiple Choice'),
        ('true_false', 'True/False'),
    )
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='single')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    question_text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500, blank=True, null=True)
    option_d = models.CharField(max_length=500, blank=True, null=True)
    correct_answer = models.CharField(max_length=10, help_text='For single: A/B/C/D, For multiple: AB/AC/ABC etc, For true/false: A(True)/B(False)')
    explanation = models.TextField(blank=True, null=True, help_text='Explanation for the correct answer')
    marks = models.IntegerField(default=1)
    image = models.ImageField(upload_to='questions/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.exam.title} - Q{self.id}"

class ExamAttempt(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'In Progress'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_attempts')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    attempt_number = models.IntegerField(default=1)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    pause_time = models.DateTimeField(blank=True, null=True)
    resume_time = models.DateTimeField(blank=True, null=True)
    time_spent = models.IntegerField(default=0, help_text='Time spent in seconds')
    score = models.FloatField(blank=True, null=True)
    percentage = models.FloatField(blank=True, null=True)
    total_questions = models.IntegerField(blank=True, null=True)
    correct_answers = models.IntegerField(blank=True, null=True)
    wrong_answers = models.IntegerField(blank=True, null=True)
    unanswered = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    rank = models.IntegerField(blank=True, null=True)
    
    class Meta:
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.student.name} - {self.exam.title}"

class StudentAnswer(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=10, help_text='For single: A/B/C/D, For multiple: AB/AC etc')
    is_correct = models.BooleanField(default=False)
    time_taken = models.IntegerField(default=0, help_text='Time taken in seconds')
    marks_obtained = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"{self.attempt.id} - Q{self.question.id}"

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ('exam_scheduled', 'Exam Scheduled'),
        ('exam_reminder', 'Exam Reminder'),
        ('result_published', 'Result Published'),
        ('achievement', 'Achievement Unlocked'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='🏆')
    points = models.IntegerField(default=0)
    criteria = models.CharField(max_length=200, help_text='e.g., complete_10_exams, score_100_percent')
    
    def __str__(self):
        return self.name

class StudentAchievement(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'achievement')
    
    def __str__(self):
        return f"{self.student.name} - {self.achievement.name}"
