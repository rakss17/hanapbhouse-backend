from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

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

    class Meta:
        model = Property
        fields = ['id', 'number_of_vacant', 'type', 'description', 'inclusion', 'rent', 'is_available', 'address']