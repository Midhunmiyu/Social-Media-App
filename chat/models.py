from django.db import models
from user.models import CustomUser

class ChatRoom(models.Model):
    name = models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class ChatMessage(models.Model):
    sender_id = models.PositiveIntegerField() # Foreign key not supported in cross-database relationships
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE,related_name='chat_rooms')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender_id}: {self.message}"