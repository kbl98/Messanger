from django.db import models
from datetime import date
from django.conf import settings

# Create your models here.
class Message (models.Model):
    text = models.CharField(max_length=1000)
    date =  models.DateField(default = date.today)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='author_message_set')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='receiver_message_set',default=None,blank=True, null=True)
    chat = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='chat_message_set',default=None,blank=True, null=True)

class User (models.Model):
    username =  models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='username_user_set')
