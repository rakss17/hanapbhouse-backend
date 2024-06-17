from rest_framework import serializers
from .models import Feed, SavedFeed
from property.serializers import PropertySerializer

class FeedSerializer(serializers.ModelSerializer):
    content = PropertySerializer()
    owner_fullname = serializers.SerializerMethodField()

    def get_owner_fullname(self, obj):
        if obj.owner:
            owner = obj.owner
            owner_fullname = f'{owner.first_name} {owner.last_name}'
            return owner_fullname
        return None

    class Meta:
        model = Feed
        fields = ['id', 'content', 'owner', 'owner_fullname', 'image', 'timestamp']

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
    
    class Meta:
        model = SavedFeed
        fields = ['id', 'content', 'owner', 'owner_fullname', 'timestamp']