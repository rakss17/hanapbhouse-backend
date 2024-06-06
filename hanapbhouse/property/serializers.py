from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    street_1 = serializers.SerializerMethodField()
    street_2 = serializers.SerializerMethodField()
    street_3 = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    province = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

    def get_street_1(self, obj):
        if obj.address:
            address = obj.address
            street_1 = address.street_1
            return street_1
        return None
    
    def get_street_2(self, obj):
        if obj.address:
            address = obj.address
            street_2 = address.street_2
            return street_2
        return None

    def get_street_3(self, obj):
        if obj.address:
            address = obj.address
            street_3 = address.street_3
            return street_3
        return None
    
    def get_city(self, obj):
        if obj.address:
            address = obj.address
            city = address.city
            return city
        return None
    
    def get_province(self, obj):
        if obj.address:
            address = obj.address
            province = address.province
            return province
        return None
    
    def get_country(self, obj):
        if obj.address:
            address = obj.address
            country = address.country
            return country
        return None
    
    def get_latitude(self, obj):
        if obj.address.coordinates:
            address = obj.address.coordinates
            latitude = address.latitude
            return latitude
        return None
    
    def get_longitude(self, obj):
        if obj.address.coordinates:
            address = obj.address.coordinates
            longitude = address.longitude
            return longitude
        return None
    
    class Meta:
        model = Property
        fields = ['number_of_vacant', 'type', 'description', 'inclusion', 'rent', 'is_available', 
                  'street_1', 'street_2', 'street_3', 'city', 'province', 'country', 'latitude', 'longitude']