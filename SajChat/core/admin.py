from django.contrib import admin
from .models import ChatMessage

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('msg_sender', 'msg_receiver', 'body', 'seen')

admin.site.register(ChatMessage, ChatMessageAdmin)