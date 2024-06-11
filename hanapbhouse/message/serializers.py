from rest_framework import serializers
from .models import Message
from django.utils.timezone import now, localtime
from django.utils.dateformat import DateFormat
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

class MessageSerializer(serializers.ModelSerializer):
    sender_fullname = serializers.SerializerMethodField()
    receiver_fullname = serializers.SerializerMethodField()

    def get_sender_fullname(self, obj):
        if obj.sender:
            sender = obj.sender
            sender_fullname = f'{sender.first_name} {sender.last_name}'
            return sender_fullname
        return None
    
    def get_receiver_fullname(self, obj):
        if obj.receiver:
            receiver = obj.receiver
            receiver_fullname = f'{receiver.first_name} {receiver.last_name}'
            return receiver_fullname
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Convert send_timestamp and read_timestamp to local timezone
        send_time_local = localtime(instance.send_timestamp)
        read_time_local = localtime(instance.read_timestamp)
        
        # Function to format time in 12-hour format
        def format_time(datetime_obj):
            return datetime_obj.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
        
        # Function to format date and time based on conditions
        def format_date_and_time(datetime_obj):
            today = now().date()
            start_of_current_year = today.replace(month=1, day=1)
    
            # Calculate the difference in days from today to the start of the current year
            days_into_year = (today - start_of_current_year).days
            
            # Determine the date one year ago from today, considering the start of the year
            not_current_year = today - timedelta(days=days_into_year + 1)
            if datetime_obj.date() == today:
                return format_time(datetime_obj)  # Just the time for today
            elif datetime_obj >= now() - timedelta(days=7):  # Within the last 7 days
                return f"{datetime_obj.strftime('%a')} at {format_time(datetime_obj)}"  # Day abbreviation and time
            elif datetime_obj.date() >= not_current_year:  # Within current year but more than 7 days ago
                day = datetime_obj.day
                formatted_day = str(day) if day > 9 else f'0{day}' 
                return f"{datetime_obj.strftime('%b')} {formatted_day} at {format_time(datetime_obj)}"  # Month abbreviation, day, and time
            else:
                # Not current year or previous years, include the year in the format
                day = datetime_obj.day
                formatted_day = str(day) if day > 9 else f'0{day}'
                return f"{datetime_obj.strftime('%b')} {formatted_day}, {datetime_obj.strftime('%Y')} at {format_time(datetime_obj)}"
        
        representation['send_timestamp'] = format_date_and_time(send_time_local)
        representation['read_timestamp'] = format_date_and_time(read_time_local)
        
        return representation

    class Meta:
        model = Message
        fields = ['id', 'room_name', 'content', 'sender', 'sender_fullname', 'send_timestamp', 'receiver', 'receiver_fullname', 'read_timestamp', 'is_read_by_receiver']