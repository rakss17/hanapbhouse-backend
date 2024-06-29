from django.shortcuts import redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly

class UserProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():

            new_image = request.FILES.get('image', None)
        
            if new_image:

                if instance.image:
                    instance.image.delete()

                instance.image = new_image
            else:
                
                if instance.image:
                    instance.image.delete()

            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)
    

