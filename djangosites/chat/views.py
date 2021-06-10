from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Message, Notification, Room, Sayi
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
@login_required(login_url = 'login')
def index(request):
    rooms = Room.objects.filter(users=request.user)
    for roomx in rooms:
        bildirimsayisi = Notification.objects.filter(message__room=roomx).exclude(message__user=request.user).count()
        sayi = Sayi.objects.filter(room=roomx).exclude(user=request.user).update(say=bildirimsayisi)
    users = User.objects.all().exclude(username=request.user.username)
    context = {
        'rooms':rooms,
        'users':users,
    }
    return render(request, 'chat/index.html', context)
@csrf_exempt
def goruldu(request,room_name):
    room = Room.objects.get(id=room_name)
    Notification.objects.filter(message__room=room).exclude(message__user=request.user).delete()
    Message.objects.filter(room=room).exclude(user=request.user).update(okundu=True)
    rooms = Room.objects.filter(users=request.user)
    for roomx in rooms:
        bildirimsayisi = Notification.objects.filter(message__room=roomx).exclude(message__user=request.user).count()
        sayi = Sayi.objects.filter(room=roomx).exclude(user=request.user).update(say=bildirimsayisi)
    context = {'rooms':rooms,}
    data =  render_to_string('chat/main.html',context=context,request=request)
    return JsonResponse({'data':data})
@csrf_exempt
def okundumu(request,room_name):
    room = Room.objects.get(id=room_name)
    try:
        mesage = Message.objects.filter(room=room, user = request.user).order_by("-date")[0]
        if mesage.okundu:
            return JsonResponse({'data':"True"})
        else:
            return JsonResponse({'data':"False"})
    except:
        return JsonResponse({'data':"Yokki"})
@login_required(login_url = 'djangosites:login')
def room(request, room_name):
    rooms = Room.objects.filter(users=request.user)
    room = Room.objects.get(id=room_name)
    Notification.objects.filter(message__room=room).exclude(message__user=request.user).delete()
    messages = Message.objects.filter(room=room)
    Message.objects.filter(room=room,).exclude(user=request.user).update(okundu=True)
    sayi = Sayi.objects.filter(room=room).exclude(user=request.user).update(say=0)
    users = User.objects.all().exclude(username=request.user.username)

    return render(request, 'chat/roomv2.html', {
        'users':users,
        'room_name': room_name,
        'room':room,
        'rooms':rooms,
        'messages':messages,
    })
def start_chat(request,username):
    secont_user = User.objects.get(username=username)
    room = Room.objects.filter(users=request.user).filter(users=secont_user)
    if len(room)==0:
        room = Room.objects.create()
        room.users.add(request.user,secont_user)
        room.save()
        Sayi.objects.create(user=request.user,room=room)
        Sayi.objects.create(user=secont_user,room=room)
        return redirect('room',room.id)
    return redirect('room',room[0].id)

@csrf_exempt
def roomcontrol(request):
    rooms = Room.objects.filter(users=request.user)
    for room in rooms:
        bildirimsayisi = Notification.objects.filter(message__room=room).exclude(message__user=request.user).count()
        sayi = Sayi.objects.filter(room=room).exclude(user=request.user).update(say=bildirimsayisi)
        Message.objects.filter(room=room,).exclude(user=request.user).update(okundu=True)

    context = {
        'rooms':rooms,
    }
    data =  render_to_string('chat/main.html',context=context,request=request)
    return JsonResponse({'data':data})