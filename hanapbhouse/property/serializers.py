from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    landlord_fullname = serializers.SerializerMethodField()

    def get_address(self, obj):
        if obj.address and obj.coordinates:
            address = obj.address
            coordinates = obj.coordinates
            return {
                'street_1': address.street_1,
                'street_2': address.street_2,
                'street_3': address.street_3,
                'city': address.city,
                'province': address.province,
                'country': address.country,
                'latitude': coordinates.latitude,
                'longitude': coordinates.longitude,
            }
        return None
    
    def get_landlord_fullname(self, obj):
        if obj.landlord:
            landlord = obj.landlord
            landlord_fullname = f'{landlord.first_name} {landlord.last_name}'

            return landlord_fullname
        return None

    class Meta:
        model = Property
        fields = ['id', 'landlord', 'landlord_fullname','number_of_vacant', 'type', 'description', 'inclusion', 'rent', 'is_available', 'address']