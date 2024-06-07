from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    landlord_full_name = serializers.SerializerMethodField()

    def get_address(self, obj):
        if obj.address:
            address = obj.address
            return {
                'street_1': address.street_1,
                'street_2': address.street_2,
                'street_3': address.street_3,
                'city': address.city,
                'province': address.province,
                'country': address.country,
                'latitude': address.coordinates.latitude if address.coordinates else None,
                'longitude': address.coordinates.longitude if address.coordinates else None,
            }
        return None
    
    def get_landlord_full_name(self, obj):
        if obj.landlord:
            landlord = obj.landlord
            landlord_full_name = f'{landlord.first_name} {landlord.last_name}'

            return landlord_full_name
        return None

    class Meta:
        model = Property
        fields = ['id', 'landlord', 'landlord_full_name','number_of_vacant', 'type', 'description', 'inclusion', 'rent', 'is_available', 'address']