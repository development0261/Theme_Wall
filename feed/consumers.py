import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Messages
from users.models import Profile,CustomeUser
from django.contrib.auth import get_user_model
from datetime import datetime
from django.core import serializers
from django.db.models import F
User=get_user_model()
from channels.db import database_sync_to_async
class ChatConsumer(WebsocketConsumer):
    response = {}
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        user = self.scope['user']
        self.accept()
        user1 = CustomeUser.objects.get(pk=user.pk)
        user1.social_status= 1
        user1.save()

    def disconnect(self, close_code):

        # Leave room group
        
        user = self.scope['user']
        user1 = CustomeUser.objects.get(pk=user.pk)
        user1.social_status= 0
        user1.save()
        async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    
                    'command': 'dectivate_user',
                    'pk':user1.pk,
                    
                }
            )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print("Disconneted")
        print("Disconneted")

        

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if text_data_json['command'] == 'new_message':
            message = text_data_json['message']
            name = text_data_json['from']

            sender = User.objects.filter(username=name)[0]

            chat = Messages(sender=sender, comment=message)
            chat.save()
            udata = Profile.objects.get(user=sender)


            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'name':name,
                    'image_url':udata.image.url,
                    'timestamp':chat.timestamp,
                    'command':text_data_json['command']
                }
            )

        elif text_data_json['command']=="fetch_old":
            messages = []
            msgs = Messages.objects.order_by('-timestamp').filter()

            for m in msgs:
                user = m.sender
                udata = Profile.objects.get(user=user)
                messages.append({'name': m.sender.username, 'content': m.comment,'image_url':udata.image.url,'timestamp':m.timestamp.strftime("%m/%d/%Y, %I:%M %p")})
                
                self.response = json.dumps({"messages": messages}, default=str)
           
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'messages':self.response,
                    'command': text_data_json['command'],
                    's_name':text_data_json['name'],
                    
                }
            )

        elif text_data_json['command'] == 'activate_user':
            print("Activate User")
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    
                    'command': text_data_json['command'],
                    'pk':text_data_json['pk'],
                    
                }
            )
        
        elif text_data_json['command'] == 'dectivate_user':
            print("dectivate User")
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    
                    'command': text_data_json['command'],
                    'pk':text_data_json['pk'],
                    
                }
            )
    # Receive message from room group
    def chat_message(self, event):

        command=event['command']
        if(command == 'new_message'):
            message = event['message']
            name = event['name']
            timestamp = event['timestamp']
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'message': message,
                'name':name,
                'image_url':event['image_url'],
                'command':command,
                'timestamp':timestamp.strftime("%m/%d/%Y, %I:%M %p")
            }))
        elif command == 'activate_user':
            self.send(text_data=json.dumps({
                'command':command,
                'pk':event['pk'],
                
            }))
        elif command == 'dectivate_user':
            self.send(text_data=json.dumps({
                'command':command,
                'pk':event['pk'],
                
            }))
        else:
            self.send(text_data=json.dumps({
                'messages':self.response,
                'command': command,
                's_name':event['s_name'],
                
            }))

    @database_sync_to_async
    def update_user_incr(self, user):
        CustomeUser.objects.filter(pk=user.pk).update(social_status=F('social_status') + 1)
        print(CustomeUser.objects.filter(pk=user.pk).social_status)

    @database_sync_to_async
    def update_user_decr(self, user):
        CustomeUser.objects.filter(pk=user.pk).update(social_status=F('social_status') - 1)