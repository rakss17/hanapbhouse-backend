import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, UserChannelTracking
from accounts.models import User
from django.utils import timezone
from channels.db import database_sync_to_async
from .serializers import MessageSerializer, UserChannelTracking
from django.contrib.auth.models import AnonymousUser

class MessageConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        # Fetching channel name from the url, the channel name pattern should be (user_id1)_(user_id2)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Fetching user id from the url to create a own channel
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        
        # Authentication for authenticated user with JWT Token
        if isinstance(self.scope['user'], AnonymousUser):      
            await self.close()
        else:
            # Join room group with the channel name and user id fetch from the url
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.channel_layer.group_add(self.user_id, self.channel_name)
            await self.accept()

            # Create a User Channel Tracking instance
            await self.create_channel(self.room_group_name)

            # function for reading incoming messages and sending to the sender's channel
            read_messages = await self.get_read_messages_by_receiver(self.user_id)
            if read_messages is not None:
                for message in read_messages:
                    sender_user_id = message['sender']  
                    await self.channel_layer.group_send(
                        sender_user_id,
                        {
                            'type': 'send_update_message', 
                            'action': 'read_message',
                            'message_id': message['id'],
                            'content': message['content'], 
                            'read_timestamp': message['read_timestamp'],
                            'is_read_by_receiver': message['is_read_by_receiver'],
                            'sender_fullname': message['sender_fullname'],
                            'receiver_fullname': message['receiver_fullname']
                            
                        }
                    )

    # function for creating channel and saving it to database
    @database_sync_to_async
    def create_channel(self, channel_name):
        user = self.user_id
        filtered_channel_tracking = UserChannelTracking.objects.filter(user=user)
        if not filtered_channel_tracking.exists():
            created_channel = UserChannelTracking.objects.create(channel_name=channel_name, user=user)

            return UserChannelTracking(created_channel)
        else:
            print({user}, "has already joined channel named: ", {channel_name})
    
    # function for updating unread messages to read message when receiver connect to the channel
    @database_sync_to_async
    def get_read_messages_by_receiver(self, user_id):
        time_now = timezone.localtime(timezone.now())
        filtered_by_receiver = Message.objects.filter(receiver=user_id)
        messages_data = []
        for filtered in filtered_by_receiver:
            if filtered.is_read_by_receiver == False and filtered.read_timestamp is None:
                filtered.is_read_by_receiver = True
                filtered.read_timestamp = time_now
                filtered.save()
                messages_data.append(MessageSerializer(filtered).data)

        return messages_data
            
    
    # leaving channel and deleting channel from database
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_discard(self.user_id, self.channel_name)
        delete_channel = await self.delete_channel()
        print(delete_channel)

    # function for deleting channel from database
    @database_sync_to_async
    def delete_channel(self):
        filtered_channel = UserChannelTracking.objects.filter(channel_name=self.room_group_name, user=self.user_id)
        if filtered_channel.exists():
            filtered_channel.delete()
            return f"{self.user_id} has been disconnected from channel: {self.room_group_name}"

    # receives and process the incoming messages
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        receiver = text_data_json['receiver']

        # fetching sender and receiver instances and utilize it for creating messages
        sender_obj = await self.get_sender_obj(sender)
        receiver_obj = await self.get_receiver_obj(receiver)
        message_obj = await self.create_message(self.room_name, message, sender_obj, receiver_obj)

        # function for reading incoming messages and sending to the sender's channel
        # use for reading messages when the receiver still connected to the channel together with the sender
        read_messages = await self.get_read_messages_by_sender(receiver)
        if read_messages is not None:
            for message in read_messages:
                sender_user_id = message['sender']  
                await self.channel_layer.group_send(
                    sender_user_id,
                    {
                        'type': 'send_update_message', 
                        'action': 'read_message',
                        'message_id': message['id'],
                        'content': message['content'], 
                        'read_timestamp': message['read_timestamp'],
                        'is_read_by_receiver': message['is_read_by_receiver'],
                        'sender_fullname': message['sender_fullname'],
                        'receiver_fullname': message['receiver_fullname']
                        
                    }
                )
        
        # sending created message to the room group channel for real-time messaging
        message_obj_filtered_id = message_obj['id']
        message_obj_filtered = await self.get_created_message_filtered(message_obj_filtered_id)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_id': message_obj_filtered['id'],
                'room_name': message_obj_filtered['room_name'],
                'content': message_obj_filtered['content'], 
                'sender_id': message_obj_filtered['sender'],
                'sender_fullname': message_obj_filtered['sender_fullname'],
                'send_timestamp': message_obj_filtered['send_timestamp'],
                'receiver_id': message_obj_filtered['receiver'],
                'receiver_fullname': message_obj_filtered['receiver_fullname'],
                'read_timestamp': message_obj_filtered['read_timestamp'],
                'is_read_by_receiver': message_obj_filtered['is_read_by_receiver']
            }
        )

        
    # fetching sender and receiver instances
    @database_sync_to_async
    def get_sender_obj(self, sender):
        user_instance = User.objects.get(id=sender)
        return user_instance
    @database_sync_to_async
    def get_receiver_obj(self, receiver):
        user_instance = User.objects.get(id=receiver)
        return user_instance
    
    # functions for creating message and save to database
    @database_sync_to_async
    def create_message(self, room_name, message, sender_obj, receiver_obj):
        queryset = Message.objects.create(room_name=room_name, content=message, sender=sender_obj, receiver=receiver_obj)
        return MessageSerializer(queryset).data
    
    # updating unread messages to read messages when receiver still connected to the channel
    @database_sync_to_async
    def get_read_messages_by_sender(self, user_id):
        time_now = timezone.localtime(timezone.now())

        # use to identify receiver's user id and fetching it from user channel tracking model database
        receiver_in_channel = None
        get_channel = UserChannelTracking.objects.filter(channel_name=self.room_group_name, user=user_id)
        if get_channel.exists():
            first_user_get_channel = get_channel.first()
            receiver_in_channel = first_user_get_channel.user

        filtered_by_receiver = Message.objects.filter(receiver=user_id)
        messages_data = []

        for filtered in filtered_by_receiver:
            if filtered.is_read_by_receiver == False and filtered.read_timestamp is None and filtered.receiver.id == receiver_in_channel:
                filtered.is_read_by_receiver = True
                filtered.read_timestamp = time_now
                filtered.save()
                messages_data.append(MessageSerializer(filtered).data)

        return messages_data
    
    # fetching the serialized created message
    @database_sync_to_async
    def get_created_message_filtered(self, message_id):
        filtered_by_room_name = Message.objects.filter(id=message_id).first()
        return MessageSerializer(filtered_by_room_name).data

    # function for reading unread messages json dumping to the channel
    async def send_update_message(self, event):
        try:
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'action': event['action'],
                'message_id': event['message_id'],  
                'content': event['content'], 
                'sender_fullname': event['sender_fullname'],
                'receiver_fullname': event['receiver_fullname'],
                'read_timestamp': event['read_timestamp'],
                'is_read_by_receiver': event['is_read_by_receiver']
            }))
            
        except Exception as e:
            print(f"Error sending message: {e}")

    # function for sending messages json dumping to the channel
    async def chat_message(self, event):
        try:
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