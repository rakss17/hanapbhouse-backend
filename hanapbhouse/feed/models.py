from django.db import models
from accounts.models import User
from property.models import Property
import secrets
import string

def generate_custom_id():
    segment_length = 5
    num_segments = 3
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    segments = [''.join(secrets.choice(characters) for _ in range(segment_length)) for _ in range(num_segments)]
    return '-'.join(segments)

class Feed(models.Model):
    id = models.CharField(primary_key=True, max_length=17, default=generate_custom_id, editable=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="feed_owner")
    content = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True, related_name="feed_content")
    image = models.ImageField(upload_to="feed_images/", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.owner.username