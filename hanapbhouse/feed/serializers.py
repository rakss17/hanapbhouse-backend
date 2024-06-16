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
    content = serializers.SerializerMethodField()
    owner_fullname = serializers.SerializerMethodField()

    def get_content(self, obj):
        if obj.content:
            feed_data = obj.content
            property_data = obj.content.content
            address = property_data.address if property_data.address else None
            # convert money field to a str to serialize it to json properly
            rent_amount = str(property_data.rent.amount) if property_data.rent else None
            return {
                'feed_owner': feed_data.owner.id,
                'feed_owner_fullname': f'{feed_data.owner.first_name} {feed_data.owner.last_name}',
                'feed_image': feed_data.image.url if feed_data.image else None,
                'feed_timestamp': feed_data.timestamp,
                'feed_property_data': {
                    'id': property_data.id,
                    'number_of_vacant': property_data.number_of_vacant,
                    'type': property_data.type,
                    'description': property_data.description,
                    'inclusion': property_data.inclusion,
                    'rent': rent_amount,
                    'is_available': property_data.is_available,
                    'address': {
                        'street_1': address.street_1,
                        'street_2': address.street_2,
                        'street_3': address.street_3,
                        'city': address.city,
                        'province': address.province,
                        'country': address.country,
                        'latitude': property_data.coordinates.latitude if property_data.coordinates else None,
                        'longitude': property_data.coordinates.longitude if property_data.coordinates else None,
                    }
                },
                
            }
        return None
    
    def get_owner_fullname(self, obj):
        if obj.owner:
            owner = obj.owner
            owner_fullname = f'{owner.first_name} {owner.last_name}'
            return owner_fullname
        return None
    
    class Meta:
        model = SavedFeed
        fields = ['id', 'content', 'owner', 'owner_fullname', 'timestamp']