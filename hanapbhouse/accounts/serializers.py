from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username', 'email', 'first_name', 'last_name', 'password', 'contact_number', 'gender', 'image']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        password = validated_data.get('password')
        contact_number = validated_data.get('contact_number')
        gender = validated_data.get('gender')

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            contact_number=contact_number,
            gender=gender
        )
        
        user.is_active = False
        user.save()
        return user

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
