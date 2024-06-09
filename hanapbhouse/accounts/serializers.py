from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    contact_number = serializers.IntegerField()
    gender = serializers.CharField()

    class Meta:
        model = User
        fields = ['id','username', 'email', 'first_name', 'last_name', 'password', 'contact_number', 'gender']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def save(self, **kwargs):
        user = User.objects.create_user(
                username=self.validated_data['username'],
                email=self.validated_data['email'],
                first_name=self.validated_data['first_name'],
                last_name=self.validated_data['last_name'],
                password=self.validated_data['password'],
                contact_number=self.validated_data['contact_number'],
                gender=self.validated_data['gender'],
            )

        user.is_active = False
        user.save()

        return user