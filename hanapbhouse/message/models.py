from django.db import models
from accounts.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="message_sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="message_receiver")
    content = models.TextField(null=True, blank=True)
    send_timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    read_timestamp = models.DateTimeField(null=True, blank=True)
    is_read_by_receiver = models.BooleanField(default=False)

    def __str__(self):
        return self.sender.username 