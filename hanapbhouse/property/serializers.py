from rest_framework import serializers
from .models import Property, Address, Coordinates

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    coordinates = CoordinatesSerializer()
    landlord_fullname = serializers.SerializerMethodField()

    def get_landlord_fullname(self, obj):
        if obj.landlord:
            return f'{obj.landlord.first_name} {obj.landlord.last_name}'
        return None

    class Meta:
        model = Property
        fields = ['id', 'landlord', 'landlord_fullname', 'number_of_vacant', 'type', 'description', 'inclusion', 'rent', 'is_available', 'address', 'coordinates']

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        coordinates_data = validated_data.pop('coordinates', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if address_data:
            address_instance = instance.address
            for attr, value in address_data.items():
                setattr(address_instance, attr, value)
            address_instance.save()

        if coordinates_data:
            coordinates_instance = instance.coordinates
            for attr, value in coordinates_data.items():
                setattr(coordinates_instance, attr, value)
            coordinates_instance.save()

        instance.save()
        return instance