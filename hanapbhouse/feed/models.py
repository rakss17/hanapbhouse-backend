from django.db import models
from accounts.models import User
from property.models import Property

class Feed(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="feed_owner")
    content = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True, related_name="feed_content")
    image = models.ImageField(upload_to="feed_images/", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.owner.username