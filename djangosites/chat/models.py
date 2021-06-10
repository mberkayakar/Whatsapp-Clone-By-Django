from django.db import models
import uuid
from django.contrib.auth.models import User
# mesaj modeli, oda modeli, chatuser

class Sayi(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    say = models.IntegerField(default=0)
    def __str__(self):
        return str(self.say)
class Room(models.Model):
    id= models.UUIDField(primary_key=True,default=uuid.uuid4)
    users = models.ManyToManyField(User)
    date = models.DateTimeField(auto_now=True)
    sayi = models.ManyToManyField(Sayi)
class Message(models.Model):
    user = models.ForeignKey(User,related_name="messages",verbose_name="kullanıcı", on_delete=models.SET_NULL,null=True)
    room = models.ForeignKey(Room, related_name='messages', verbose_name="oda", on_delete=models.SET_NULL,null=True)
    content = models.TextField(verbose_name="mesak içeriği")
    what_is_it=models.CharField(max_length=50, null=True)
    file = models.FileField(upload_to="", null=True)
    okundu = models.BooleanField(default=False)
    date = models.DateTimeField()
class Notification(models.Model):
    message = models.OneToOneField(Message, on_delete=models.DO_NOTHING)
class Profile(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.SET_NULL)
    online = models.BooleanField(default=False)
    sontarih = models.DateTimeField(auto_now = True)
from django.db.models.signals import pre_save
from datetime import date, datetime
def date_save(sender,instance,*args,**kwargs):
    instance.room.date=datetime.now()
    instance.room.save()
pre_save.connect(date_save, sender=Message)