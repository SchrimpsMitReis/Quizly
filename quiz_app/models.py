from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Quiz(models.Model):
    """
    Model representing a quiz generated from a YouTube video.
    Each quiz belongs to a user and contains multiple questions.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.CharField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizer')
    
    def __str__(self):
        """
        Return a readable representation of the quiz.
        """
        return f"Quiz {self.id}, {self.title}  by {self.user.username}"


class Question(models.Model):
    """
    Model representing a single quiz question.
    Each question belongs to a quiz and contains multiple answer options.
    """
    question_title = models.TextField(max_length=200)
    question_options = models.JSONField()
    answer = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    
    def __str__(self):
        """
        Return a readable representation of the question.
        """
        return f"Quiz  {self.quiz.title} - {self.question_title}"