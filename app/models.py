from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Survey(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Question(models.Model):
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text

class Response(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    survey = models.ForeignKey(Survey, related_name='responses', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice,related_name='responses' , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response: {self.choice.text} to {self.question.text} question of {self.survey.title} survey"
    
    def save(self, *args, **kwargs):
        if self.question.survey != self.survey:
            raise ValueError('Question does not belong to the selected survey')
        if self.choice.question != self.question:
            raise ValueError('Choice does not belong to the selected question')
        super().save(*args, **kwargs)