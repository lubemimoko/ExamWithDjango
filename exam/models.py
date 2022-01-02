from django.db import models
from examProject import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
levels = (("Easy", "Easy"), ("Medium", "Medium"), ("Hard","Hard"))


class Student(AbstractUser):
    studentId = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=11, unique=True) 
    email = models.EmailField(unique=True, blank=True, max_length=254, verbose_name='email address')  
    # image = models.ImageField(upload_to="upload_image", null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'auth_user'

      

class Course(models.Model):
    course = models.CharField(max_length=20, unique=True)
    datetime = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return str(self.course)

class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="topics")
    topic = models.CharField(max_length=30)
    datetime = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'topic'], name='coursetopic')
        ]  
    
    def __str__(self):
        return f"{self.topic}"


class Exam(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="exams")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="exams")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name= "exams")
    level = models.CharField(max_length=20, choices=levels)
    number_of_questions = models.IntegerField()
    no_ques_attempt = models.IntegerField(default=0)
    no_ques_right = models.IntegerField(default=0)
    total_marks = models.CharField(max_length=20, default=0)
    time_duration = models.IntegerField(default=0, help_text="duration of the exam in minutes")
    start_time = models.DateTimeField(auto_now=True)
    datetime = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return str(self.student)

    # def save(self, *a, **k):
    #     self.time_duration = (1.30 * self.number_of_questions)

    #     return super().save(*a, **k)

    def get_questions(self):
        return self.questions.all()[:self.number_of_questions]           

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="questions")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name= "questions")
    level = models.CharField(max_length=20, choices=levels)
    text = models.TextField(max_length=500)
    datetime = models.DateTimeField(auto_now_add=True, editable=False)

    
    def __str__(self):
        return str(self.text)
    
    @property
    def get_answers(self):
        return self.answers.all() 


class Answer(models.Model):
    text = models.TextField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    datetime = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"





class Result(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.pk)
    
#vicky-good, israel-all good, Omot-good