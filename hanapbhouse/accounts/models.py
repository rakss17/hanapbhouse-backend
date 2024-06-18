from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from utils.helpers import generate_custom_id
import os

class User(AbstractUser):
    id = models.CharField(primary_key=True, max_length=17, default=generate_custom_id, editable=False, unique=True)
    contact_number = models.BigIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="profile_images/", null=True, blank=True)

    def __str__(self):
        return self.username


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if sender.name == 'accounts':
        Custom_User = User
        username = os.getenv('DJANGO_ADMIN_USERNAME')
        email = os.getenv('DJANGO_ADMIN_EMAIL')
        password = os.getenv('DJANGO_ADMIN_PASSWORD')

        if not Custom_User.objects.filter(username=username).exists():
            
            superuser = Custom_User.objects.create_superuser(
                username=username, email=email, password=password)

            superuser.is_active = True
            print('Created admin account')
            superuser.save()