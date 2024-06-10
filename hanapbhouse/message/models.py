from django.db import models
from accounts.models import User
import uuid

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_name = models.CharField(max_length=255, null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="message_sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="message_receiver")
    content = models.TextField(null=True, blank=True)
    send_timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    read_timestamp = models.DateTimeField(null=True, blank=True)
    is_read_by_receiver = models.BooleanField(default=False)

    def __str__(self):
        return self.sender.username

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="notification_owner")
    subject = models.CharField(max_length=1000, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.owner.username 