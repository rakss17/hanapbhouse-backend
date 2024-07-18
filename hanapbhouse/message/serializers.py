from rest_framework import serializers
from .models import Message, UserChannelTracking
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _
from utils.helpers import format_date_and_time
from drf_spectacular.utils import extend_schema_field
from typing import Optional

class MessageSerializer(serializers.ModelSerializer):
    sender_fullname = serializers.SerializerMethodField()
    sender_image =  serializers.SerializerMethodField()
    receiver_fullname = serializers.SerializerMethodField()
    receiver_image = serializers.SerializerMethodField()

    def get_sender_fullname(self, obj) -> Optional[str]:
        if obj.sender:
            sender = obj.sender
            sender_fullname = f'{sender.first_name} {sender.last_name}'
            return sender_fullname
        return None
    
    def get_receiver_fullname(self, obj) -> Optional[str]:
        if obj.receiver:
            receiver = obj.receiver
            receiver_fullname = f'{receiver.first_name} {receiver.last_name}'
            return receiver_fullname
        return None
    
    @extend_schema_field(serializers.ImageField())
    def get_sender_image(self, obj) -> Optional[str]:
        if obj.sender.image:
            image_path = obj.sender.image.name
            sender_image = f"media/{image_path}"
            return sender_image
        return None
    
    @extend_schema_field(serializers.ImageField())
    def get_receiver_image(self, obj) -> Optional[str]:
        if obj.receiver.image:
            image_path = obj.receiver.image.name
            receiver_image = f"media/{image_path}"
            return receiver_image
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Convert send_timestamp and read_timestamp to local timezone
        send_time_local = localtime(instance.send_timestamp)
        read_time_local = None
        if instance.read_timestamp:
            read_time_local = localtime(instance.read_timestamp)
        else:
            read_time_local = None
        
        serializer_type = "message"
        representation['send_timestamp'] = format_date_and_time(send_time_local, serializer_type)
        representation['read_timestamp'] = format_date_and_time(read_time_local, serializer_type)
        
        return representation

    class Meta:
        model = Message
        fields = ['id', 'room_name', 'content', 'sender', 'sender_fullname', 'send_timestamp', 'receiver', 'receiver_fullname', 'read_timestamp', 'is_read_by_receiver', 'sender_image', 'receiver_image']

class UserChannelTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChannelTracking
        fields = '__all__'