
from django.shortcuts import render,redirect
from .models import Message,User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import  RegisterForm
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
@login_required(login_url='/login/')

def chatindex(request):
    if request.method == 'POST':
        print('This request:'+request.POST['textmessage'])
        receiver_username = request.POST['receiver']
        receiver_user = User.objects.get(username=receiver_username)
        new_message=Message.objects.create(text = request.POST['textmessage'],author=request.user, receiver =receiver_user.id)
        chatUsers=User.objects.all()
        return render (request,'chat/chatindex.html',{'users':chatUsers})
    if request.method == 'GET':
        chatUsers=User.objects.all()
        print(chatUsers)
        return render (request,'chat/chatindex.html',{'users':chatUsers})

def loginindex(request):
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
    if request.method == 'GET':
        form = RegisterForm()
        return render (request,'registration/registrationindex.html',{'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            User.objects.create(username=user)
            login(request, user)
            return HttpResponseRedirect ('/chat/')
        else:
            return render(request,'registration/registrationindex.html',{'form': form} )
     