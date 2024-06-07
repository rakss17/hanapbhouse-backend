from rest_framework import serializers
from .models import Feed

class FeedSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    owner_fullname = serializers.SerializerMethodField()

    def get_content(self, obj):
        if obj.content:
            content = obj.content
            address = obj.content.address if obj.content.address else None
            # convert money field to a str to serialize it to json properly
            rent_amount = str(content.rent.amount) if content.rent else None
            return {
                'id': content.id,
                'number_of_vacant': content.number_of_vacant,
                'type': content.type,
                'description': content.description,
                'inclusion': content.inclusion,
                'rent': rent_amount,
                'is_available': content.is_available,
                'address': {
                    'street_1': address.street_1,
                    'street_2': address.street_2,
                    'street_3': address.street_3,
                    'city': address.city,
                    'province': address.province,
                    'country': address.country,
                    'latitude': address.coordinates.latitude if address.coordinates else None,
                    'longitude': address.coordinates.longitude if address.coordinates else None,
                }
            }
        return None
    
    def get_owner_fullname(self, obj):
        if obj.owner:
            owner = obj.owner
            owner_fullname = f'{owner.first_name} {owner.last_name}'
            return owner_fullname
        return None
    
    class Meta:
        model = Feed
        fields = ['id', 'content', 'owner', 'owner_fullname','image']