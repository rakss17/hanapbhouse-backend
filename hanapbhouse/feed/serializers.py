from rest_framework import serializers
from .models import Feed, SavedFeed
from property.serializers import PropertySerializer
from django.utils.timezone import localtime
from utils.helpers import format_date_and_time

class FeedSerializer(serializers.ModelSerializer):
    content = PropertySerializer()
    owner_fullname = serializers.SerializerMethodField()
    owner_image = serializers.SerializerMethodField()

    def get_owner_fullname(self, obj):
        if obj.owner:
            owner = obj.owner
            owner_fullname = f'{owner.first_name} {owner.last_name}'
            return owner_fullname
        return None
    
    def get_owner_image(self, obj):
        if obj.owner:
            owner = obj.owner
            owner_image = owner.image.url
            return owner_image
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Convert send_timestamp and read_timestamp to local timezone
        time_local = localtime(instance.timestamp)
        
        serializer_type = "other"
        representation['timestamp'] = format_date_and_time(time_local, serializer_type)
        
        return representation

    class Meta:
        model = Feed
        fields = ['id', 'content', 'owner', 'owner_fullname', 'image', 'timestamp', 'owner_image']

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
    
    def get_owner_fullname(self, obj):
        if obj.owner:
            owner = obj.owner
            owner_fullname = f'{owner.first_name} {owner.last_name}'
            return owner_fullname
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Convert send_timestamp and read_timestamp to local timezone
        time_local = localtime(instance.timestamp)
        
        serializer_type = "other"
        representation['timestamp'] = format_date_and_time(time_local, serializer_type)
        
        return representation
    
    class Meta:
        model = SavedFeed
        fields = ['id', 'content', 'owner', 'owner_fullname', 'timestamp']