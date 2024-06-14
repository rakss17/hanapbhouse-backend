from django.db import models
from accounts.models import User
from property.models import Property
from functions.generate_custom_id import generate_custom_id

class Feed(models.Model):
    id = models.CharField(primary_key=True, max_length=17, default=generate_custom_id, editable=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="feed_owner")
    content = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True, related_name="feed_content")
    image = models.ImageField(upload_to="feed_images/", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.owner.username
    
class SavedFeed(models.Model):
    id = models.CharField(primary_key=True, max_length=17, default=generate_custom_id, editable=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="savedfeed_owner")
    content = models.ForeignKey(Feed, on_delete=models.CASCADE, null=True, blank=True, related_name="savedfeed_content")
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.owner.username