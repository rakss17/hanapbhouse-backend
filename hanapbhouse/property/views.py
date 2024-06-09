from rest_framework.permissions import IsAuthenticated
from decimal import Decimal, InvalidOperation
from rest_framework import generics
from rest_framework.response import Response
from .models import Address, Coordinates, Property
from .serializers import PropertySerializer
from accounts.models import User

# PROPERTY CREATION AND LISTING
class PropertListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PropertySerializer

    def get_queryset(self):
        return Property.objects.filter(landlord=self.request.user)

    def create(self, request, *args, **kwargs):
        # Address data from HTTP Post Request
        street_1 = request.data.get('street_1')
        street_2 = request.data.get('street_2')
        street_3 = request.data.get('street_3')
        city = request.data.get('city')
        province = request.data.get('province')
        country = request.data.get('country')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        # Convert latitude and longitude type to decimal
        try:
            latitude = Decimal(latitude)
            longitude = Decimal(longitude)
        except (ValueError, InvalidOperation):
            return Response({"error": "Invalid latitude or longitude values."}, status=400)

        # Property data from HTTP Post Request
        landlord = request.data.get('landlord')
        number_of_vacant = request.data.get('number_of_vacant')
        property_type = request.data.get('type')
        description = request.data.get('description')
        inclusion = request.data.get('inclusion')
        rent = request.data.get('rent')

        # Address model instance creation

        address_created = None
        address_filtered_from_db = Address.objects.filter(street_1=street_1, street_2=street_2, street_3=street_3, 
                                      city=city, province=province, country=country)
        if not address_filtered_from_db.exists():
            address = Address.objects.create(
                street_1=street_1,
                street_2=street_2,
                street_3=street_3,
                city=city,
                province=province,
                country=country,
                
            )
            address_created = address
        else:
            address_created = address_filtered_from_db.first()

        coordinates_created = None
        coordinates_filtered_from_db = Coordinates.objects.filter(latitude=latitude, longitude=longitude)
        if not coordinates_filtered_from_db.exists():
            coordinates = Coordinates.objects.create(latitude=latitude, longitude=longitude)
            coordinates_created = coordinates
        else:
            coordinates_created = coordinates_filtered_from_db.first()

        landlord_instance = User.objects.get(id=landlord)

        # Property model instance creation
        property_created = Property.objects.create(
            landlord=landlord_instance,
            address=address_created,
            coordinates=coordinates_created,
            number_of_vacant=number_of_vacant,
            type=property_type,
            description=description,
            inclusion=inclusion,
            rent=rent
        )
        property_created.save()

        return Response({"message": "Property successfully created."}, status=201)