from django.db import models
from djmoney.models.fields import MoneyField
from accounts.models import User

class Address(models.Model):
    street_1 = models.CharField(max_length=1000, null=True, blank=True)
    street_2 = models.CharField(max_length=1000, null=True, blank=True)
    street_3 = models.CharField(max_length=1000, null=True, blank=True)
    city = models.CharField(max_length=1000, null=True, blank=True)
    province = models.CharField(max_length=1000, null=True, blank=True)
    country = models.CharField(max_length=1000, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f'{self.street_1}, {self.street_2}'

class Property(models.Model):
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="property_landlord")
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True, related_name="property_address")
    number_of_slots = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    inclusion = models.CharField(max_length=255, null=True, blank=True)
    rent = MoneyField(max_digits=14, decimal_places=2, default_currency='PHP')

    def __str__(self):
        return self.landlord.username
    
class Room(models.Model):
    tenant = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True)
    is_vacant = models.BooleanField(default=True)

    def __str__(self):
        return self.tenant.username
