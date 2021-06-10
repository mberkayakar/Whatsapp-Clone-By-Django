from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth import logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate

def logins(request):
    if request.method=="POST":
        username = request.POST['username']  
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            request.session.set_expiry(12000)
            return redirect('/chat/')
    return render(request,'chat/login.html')
def cikisyap(request):
    logout(request)
    return  redirect("/")
