from rest_framework import serializers
from accounts.models import CustomUser

def validate_unique_username(value):
    if CustomUser.objects.filter(username=value).exists():
        raise serializers.ValidationError(f"{value} is already taken. Please choose another one.")

def validate_unique_email(value):
    if CustomUser.objects.filter(email=value).exists():
        raise serializers.ValidationError(f"{value} is already registered. Please log in or use a different email.")