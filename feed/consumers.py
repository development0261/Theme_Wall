import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from .models import Messages
from users.models import Profile,CustomeUser
from django.contrib.auth import get_user_model
from datetime import datetime
from django.core import serializers
from django.db.models import F
User=get_user_model()
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        user = self.scope['user']
        await database_sync_to_async(self.update_user_incr)(user)
        

    async def disconnect(self, close_code):
        # Leave room group
        user = self.scope['user']
        await database_sync_to_async(self.update_user_decr)(user)
        await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    
                    'command': 'dectivate_user',
                    'pk':user.pk,
                    
                }
            )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    def save_message(self):
        sender = User.objects.filter(username=self.name)[0]
        chat = Messages(sender=sender, comment=self.message)
        chat.save()
        return chat

      
    def update_user_incr(self, user):
        user1 = CustomeUser.objects.get(pk=user.pk)
        user1.social_status= 1
        user1.save()

    
    def update_user_decr(self, user):
        user1 = CustomeUser.objects.get(pk=user.pk)
        user1.social_status= 0
        user1.save()

    def get_image_url(self):
        sender = User.objects.filter(username=self.name)[0]
        return Profile.objects.get(user=sender).image.url

    def fetch_messages(self):
        
        messages = []
        msgs =Messages.objects.order_by('-timestamp').all()
        self.response=None
        
        for m in msgs:
            messages.append({'name': m.sender.username, 'content': m.comment,'image_url':m.sender.profile.image.url,'timestamp':m.timestamp.strftime("%m/%d/%Y, %I:%M %p")})
            self.response = json.dumps({"messages": messages}, default=str)

        async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'messages':self.response,
                    'command': self.command,
                    's_name':self.s_name,
                    
                }
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['command'] == 'new_message':
            message = text_data_json['message']
            name = text_data_json['from']
            self.message = message
            self.name = name
            chat = await database_sync_to_async(self.save_message)()
            image_url = await database_sync_to_async(self.get_image_url)()

            print(chat)
            

            # Send message to room group
            await self.channel_layer.group_send (
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'name':name,
                    'image_url':image_url,
                    'timestamp':chat.timestamp.strftime("%m/%d/%Y, %I:%M %p"),
                    'command':'new_message'
                }
            )
        
        elif text_data_json['command']=="fetch_old":
            self.command = text_data_json['command']
            self.s_name = text_data_json['name']
            await database_sync_to_async(self.fetch_messages)()

        elif text_data_json['command'] == 'activate_user':
            print("Activate User")
            await  self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    
                    'command': 'activate_user',
                    'pk':text_data_json['pk'],
                    
                }
            )
        
        elif text_data_json['command'] == 'dectivate_user':
            print("dectivate User")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    
                    'command': 'dectivate_user',
                    'pk':text_data_json['pk'],
                    
                }
            )

    async def chat_message(self, event):

        command=event['command']
        if command == 'new_message':
            
            message = event['message']
            name = event['name']
            timestamp = event['timestamp']
            
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': message,
                'name':name,
                'image_url':event['image_url'],
                'command':command,
                'timestamp':timestamp
            }))
        elif command == 'activate_user':
            await self.send(text_data=json.dumps({
                'command':command,
                'pk':event['pk'],
                
            }))
        elif command == 'dectivate_user':
            await self.send(text_data=json.dumps({
                'command':command,
                'pk':event['pk'],
                
            }))
        else:
            await self.send(text_data=json.dumps({
                'messages':self.response,
                'command': command,
                's_name':event['s_name'],
                
            }))

