from rest_framework import serializers
from .models import Feed, SavedFeed
from property.serializers import PropertySerializer
from django.utils.timezone import localtime
from utils.helpers import format_date_and_time
from drf_spectacular.utils import extend_schema_field
from django.conf import settings
from typing import Optional

class FeedSerializer(serializers.ModelSerializer):
    content = PropertySerializer()
    owner_fullname = serializers.SerializerMethodField()
    owner_image = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    saved_feed_id = serializers.SerializerMethodField()

    def get_owner_fullname(self, obj) -> Optional[str]:
        if obj.owner:
            owner = obj.owner
            owner_fullname = f'{owner.first_name} {owner.last_name}'
            return owner_fullname
        return None
    
    @extend_schema_field(serializers.ImageField())
    def get_owner_image(self, obj) -> Optional[str]:
        if obj.owner.image:
            image_path = obj.owner.image.name
            owner_image = f"media/{image_path}"
            return owner_image
        return None
    
    @extend_schema_field(serializers.ImageField())
    def get_image(self, obj) -> Optional[str]:
        if obj.image:
            image_path = obj.image.name
            image = f"media/{image_path}"
            return image
        return None
    
    def get_is_saved(self, obj) -> Optional[str]:
       
        user = self.context['request'].user

        return SavedFeed.objects.filter(content__id=obj.id, owner=user.id).exists()
    
    def get_saved_feed_id(self, obj) -> Optional[str]:
       
        user = self.context['request'].user

        try:
            saved_feed_data = SavedFeed.objects.get(content__id=obj.id, owner=user.id)
            return saved_feed_data.id
        except SavedFeed.DoesNotExist:
            return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        time_local = localtime(instance.timestamp)
        
        serializer_type = "other"
        representation['timestamp'] = format_date_and_time(time_local, serializer_type)
        
        return representation

    class Meta:
        model = Feed
        fields = ['id', 'content', 'owner', 'owner_fullname', 'image', 'timestamp', 'owner_image', 'is_saved', 'saved_feed_id']

    def update(self, instance, validated_data):
        content_data = validated_data.pop('content', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if content_data:
            property_serializer = PropertySerializer(instance.content, data=content_data, partial=True)
            property_serializer.is_valid(raise_exception=True)
            property_serializer.save()

        instance.save()
        return instance


class SavedFeedSerializer(serializers.ModelSerializer):
    content = FeedSerializer()
    owner_fullname = serializers.SerializerMethodField()
    
    def get_owner_fullname(self, obj) -> Optional[str]:
        if obj.owner:
            owner = obj.owner
            owner_fullname = f'{owner.first_name} {owner.last_name}'
            return owner_fullname
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        time_local = localtime(instance.timestamp)
        
        serializer_type = "other"
        representation['timestamp'] = format_date_and_time(time_local, serializer_type)
        
        return representation
    
    class Meta:
        model = SavedFeed
        fields = ['id', 'content', 'owner', 'owner_fullname', 'timestamp']