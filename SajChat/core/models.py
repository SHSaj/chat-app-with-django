from django.db import models
from account.models import Account

class ChatMessage(models.Model):
    body = models.TextField()
    msg_sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="msg_sender")
    msg_receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="msg_receiver")
    seen = models.BooleanField(default=False)


    def __str__(self):
        return self.body
    