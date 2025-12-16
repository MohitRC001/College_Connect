from django.db import models
from students.models import Student
import uuid

class ChatRoom(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student1 = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='chat_student1')
    student2 = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='chat_student2')

    def __str__(self):
        return f"{self.student1} & {self.student2}"

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Student, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} at {self.timestamp}"
