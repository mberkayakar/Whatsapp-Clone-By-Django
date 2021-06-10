import json
import base64, secrets, io
from typing import no_type_check
from PIL import Image
from django.core.files.base import ContentFile
from .models import *
import json
from asgiref.sync import async_to_sync 
from .models import Profile
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from channels.db import database_sync_to_async
def get_image_from_data_url( data_url, resize=True, base_width=600 ):

    _format, _dataurl       = data_url.split(';base64,')
    _filename, _extension   = secrets.token_hex(20), _format.split('/')[-1]
    file = ContentFile( base64.b64decode(_dataurl), name=f"{_filename}.{_extension}")
    
    if resize:
        image = Image.open(file)
        image_io = io.BytesIO()
        w_percent    = (base_width/float(image.size[0]))
        h_size       = int((float(image.size[1])*float(w_percent)))
        image        = image.resize((base_width,h_size), Image.ANTIALIAS)

        image.save(image_io, format=_extension)
        file = ContentFile( image_io.getvalue(), name=f"{_filename}.{_extension}" )
    return file, ( _filename, _extension )
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        user = self.scope['user']
        profil = Profile.objects.filter(user=user)[0]
        profil.online = True
        profil.save()
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        user = self.scope['user']
        profil = Profile.objects.filter(user=user)[0]
        profil.online = False
        profil.save()
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        what_is_it = text_data_json['what_is_it']
        if message=="görüldümesajı10203040":
            pass
        else:    
            if what_is_it=="text":
                user = self.scope['user']
                room = Room.objects.get(id=self.room_name)
                asd = Message.objects.create(user=user, room=room, content=message,what_is_it=what_is_it,date=datetime.now())
                bildirim = Notification.objects.create(message = asd)
                try:
                    sayi = Sayi.objects.filter(room=room).exclude(user=user)[0]
                    ssayi = sayi.say
                    sayi.say = ssayi +1
                    sayi.save()
                except:
                    print("np")
                async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'user':user.username,
                        'created_date':str(asd.date.hour)+":"+str(asd.date.minute),
                        'what_is_it':what_is_it,
                    }
                )
            else:
                user = self.scope['user']
                room = Room.objects.get(id=self.room_name)
                file = get_image_from_data_url(message)[0]
                asd = Message.objects.create(user=user, room=room, file=file,what_is_it=what_is_it,date=datetime.now())
                bildirim = Notification.objects.create(message = asd)
                sayi = Sayi.objects.filter(room=room).exclude(user=user)[0]
                ssayi = sayi.say
                sayi.say = ssayi +1
                sayi.save()
                async_to_sync(self.channel_layer.group_send)(
                    
                self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': asd.file.url,
                        'user':user.username,
                        'created_date':str(asd.date.hour)+":"+str(asd.date.minute),
                        'what_is_it':what_is_it,
                    }
                )

        # Send message to room group
        
    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user = event['user']
        created_date=event['created_date']
        
        what_is_it=event['what_is_it']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user':user,
            'created_date':created_date,
            'what_is_it':what_is_it,
        }))
        