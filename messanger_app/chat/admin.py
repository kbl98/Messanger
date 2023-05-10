from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
   fields = ('chat','text','date','author','receiver')
   list_display =('text','date','author','receiver','chat')
# Register your models here.
admin.site.register(Message,MessageAdmin)