import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from accounts.models import User
from accounts.serializers import UserSerializer
from channels.db import database_sync_to_async
from .serializers import MessageSerializer
from django.contrib.auth.models import AnonymousUser

class MessageConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        if isinstance(self.scope['user'], AnonymousUser):      
            await self.close()
        else:
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            
            # Send previous messages to WebSocket
            messages = await self.get_messages(self.room_name)
      
            for message in messages:
                await self.send(text_data=json.dumps({
                    'message_id': message['id'],
                    'room_name': message['room_name'],
                    'content': message['content'], 
                    'sender_id': message['sender'],
                    'sender_fullname': message['sender_fullname'],
                    'send_timestamp': message['send_timestamp'],
                    'receiver_id': message['receiver'],
                    'receiver_fullname': message['receiver_fullname'],
                    'read_timestamp': message['read_timestamp'],
                    'is_read_by_receiver': message['is_read_by_receiver']
                }))

    @database_sync_to_async
    def get_messages(self, room_name):
        queryset = Message.objects.filter(room_name=room_name).order_by('send_timestamp')
        return MessageSerializer(queryset, many=True).data

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            sender = text_data_json['sender']
            receiver = text_data_json['receiver']

            # Save message to database
            sender_obj = await self.get_sender_obj(sender)
            receiver_obj = await self.get_receiver_obj(receiver)
            message_obj = await self.create_message(self.room_name, message, sender_obj, receiver_obj)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_id': message_obj['id'],
                    'room_name': message_obj['room_name'],
                    'content': message_obj['content'], 
                    'sender_id': message_obj['sender'],
                    'sender_fullname': message_obj['sender_fullname'],
                    'send_timestamp': message_obj['send_timestamp'],
                    'receiver_id': message_obj['receiver'],
                    'receiver_fullname': message_obj['receiver_fullname'],
                    'read_timestamp': message_obj['read_timestamp'],
                    'is_read_by_receiver': message_obj['is_read_by_receiver']
                }
            )

        except Exception as e:
            print(f"Error processing message: {e}")

    @database_sync_to_async
    def get_sender_obj(self, sender):
        user_instance = User.objects.get(id=sender)
        return user_instance
    
    @database_sync_to_async
    def get_receiver_obj(self, receiver):
        user_instance = User.objects.get(id=receiver)
        return user_instance
    
    @database_sync_to_async
    def create_message(self, room_name, message, sender_obj, receiver_obj):
        queryset = Message.objects.create(room_name=room_name, content=message, sender=sender_obj, receiver=receiver_obj)
        return MessageSerializer(queryset).data

    async def chat_message(self, event):
        try:
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message_id': event['message_id'],
                'room_name': event['room_name'],
                'content': event['content'], 
                'sender_id': event['sender_id'],
                'sender_fullname': event['sender_fullname'],
                'send_timestamp': event['send_timestamp'],
                'receiver_id': event['receiver_id'],
                'receiver_fullname': event['receiver_fullname'],
                'read_timestamp': event['read_timestamp'],
                'is_read_by_receiver': event['is_read_by_receiver']
            }))
            
        except Exception as e:
            print(f"Error sending message: {e}")