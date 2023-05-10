
from django.shortcuts import render,redirect
from .models import Message
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
    return render (request,'chat/chatindex.html')

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
            login(request, user)
            return HttpResponseRedirect ('/chat/')
        else:
            return render(request,'registration/registrationindex.html',{'form': form} )
     