from django.db import models
from accounts.models import CustomUser
from property.models import Property
from utils.helpers import generate_custom_id

class Feed(models.Model):
    id = models.CharField(primary_key=True, max_length=25, default=generate_custom_id, editable=False, unique=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="feed_owner")
    content = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True, related_name="feed_content")
    image = models.ImageField(upload_to="feed_images/", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.owner.username
    
class SavedFeed(models.Model):
    id = models.CharField(primary_key=True, max_length=25, default=generate_custom_id, editable=False, unique=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="savedfeed_owner")
    content = models.ForeignKey(Feed, on_delete=models.CASCADE, null=True, blank=True, related_name="savedfeed_content")
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.owner.username