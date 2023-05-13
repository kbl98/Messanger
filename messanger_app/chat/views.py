
from django.shortcuts import render,redirect
from .models import Message,User2
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import  RegisterForm
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from asgiref.sync import sync_to_async



# Create your views here.
@login_required(login_url='/login/')


def chatindex(request):
    """This is a view to create a new Message Object at Backend and return the new Message to Frontend on post, on get Messages are rendered"""
    if request.method == 'POST':
        print('This request:'+request.POST['textmessage'])
        receiver_username = request.POST['receiver']
        print(receiver_username)
        receiver_user=User.objects.get(username=receiver_username)
        new_message=Message.objects.create(text = request.POST['textmessage'],author=request.user, receiver =receiver_user)
        chatUsers=User2.objects.all()
        serialized_messages=serializers.serialize('json',[new_message])
        return JsonResponse(serialized_messages[1:-1],safe=False)
        
    if request.method == 'GET':
        chatUsers=User.objects.all()
        allMessages=Message.objects.filter(Q(author=request.user) | Q(receiver=request.user) | Q(receiver__username="Alle"))
        print(chatUsers)
        return render (request,'chat/chatindex.html',{'messages':allMessages,'users':chatUsers,'user':request.user})

def loginindex(request):
    """This view logs a user in and directs to 'Chat', when login successful. Otherwise login-page is rendered"""
    if request.method == 'POST':
        print('trylogin')
        user = authenticate(username=request.POST.get('username'),password=request.POST.get('password'))
        if user:
            login(request, user) 
            return HttpResponseRedirect ('/chat/')
        else:
            return render(request,'login/loginindex.html')
    return render (request,'login/loginindex.html')

def registrationindex(request):
    """This Funktion renders a registration-form; on post user is registrated, logged-in and lead to 'chat'"""
    if request.method == 'GET':
        form = RegisterForm()
        return render (request,'registration/registrationindex.html',{'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            User2.objects.create(username=user)
            login(request, user)
            return HttpResponseRedirect ('/chat/')
        else:
            return render(request,'registration/registrationindex.html',{'form': form} )
     

@sync_to_async
def logout_view(request):
    """function for logout of user"""
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/login/')
    return render (request,'login/loginindex.html')