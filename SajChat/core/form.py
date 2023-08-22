from django import forms
from django.forms import ModelForm
from .models import ChatMessage

class ChatMessageForm(ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "rows": 1, "placeholder": "Type Message here"}))

    class Meta:
        model = ChatMessage
        fields = ["body"]