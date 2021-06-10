from django.contrib import admin
from .models import  *
admin.site.register(Notification)
admin.site.register(Profile)
admin.site.register(Room)
admin.site.register(Sayi)
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user','room','date']
    class Meta:
        model= Message