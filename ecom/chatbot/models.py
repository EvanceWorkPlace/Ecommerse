from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatSession(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_id = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

# class ChatMessage(models.Model):
    # session = models.ForeignKey(ChatSession, related_name="messages", on_delete=models.CASCADE)
    # role = models.CharField(max_length=20)  # 'user' or 'assistant' or 'system'
    # content = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)

class UploadedImage(models.Model):
    session = models.ForeignKey(ChatSession, null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='uploads/chatbot/')
    label = models.CharField(max_length=255, blank=True)  # store model prediction (if any)
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('bot', 'Bot'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role.capitalize()} - {self.message[:40]}"
