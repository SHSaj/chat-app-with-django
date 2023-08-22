from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account.models import Account, Friend
from core.form import ChatMessageForm
from core.models import ChatMessage
from django.http import JsonResponse
import json


@login_required(login_url='/login/')
def home_screen_view(request, *args, **kwargs):
    user = Account.objects.get(username=request.user)
    friends = user.friends.all()
    context = {"user": user, "friends": friends}
    return render(request, "core/home.html", context)

@login_required(login_url='/login/')
def chat_view(request, pk):
    friend = Friend.objects.get(profile_id=pk)
    user = request.user
    profile = Account.objects.get(id=friend.profile.id)
    sent_chats = ChatMessage.objects.filter(msg_sender=user, msg_receiver=profile)
    received_chats =ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)
    received_chats.update(seen=True)
    chats = sent_chats.union(received_chats)
    form = ChatMessageForm()
    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user
            chat_message.msg_receiver = profile
            chat_message.save()
            return redirect("chat", pk=friend.profile.id)
    context = {"friend": friend, "form": form,"user":user, "profile": profile, "chats": chats, "count": received_chats.count() }
    if user == profile:
        return redirect('home')
    
    friend_profile = Account.objects.get(id=pk)
    if not user.friends.filter(profile=friend_profile).exists():
        friend_instance, created = Friend.objects.get_or_create(profile=friend_profile)
        user.friends.add(friend_instance)

    return render(request, "core/chat.html", context)

@login_required(login_url='/login/')
def sentMessages(request, pk):
    user = request.user
    friend = Friend.objects.get(profile_id=pk)
    profile = Account.objects.get(id=friend.profile.id)
    data = json.loads(request.body)
    new_chat = data["msg"]
    new_chat_message = ChatMessage.objects.create(body=new_chat, msg_sender=user ,msg_receiver=profile, seen=False)
    return JsonResponse(new_chat_message.body, safe= False)

@login_required(login_url='/login/')
def receivedMessages(request, pk):
    user = request.user
    friend = Friend.objects.get(profile_id=pk)
    profile = Account.objects.get(id=friend.profile.id)
    arr = []
    chats = ChatMessage.objects.filter(msg_sender= profile, msg_receiver= user)
    for chat in chats:
        arr.append(chat.body)
    return JsonResponse(arr, safe= False)

@login_required(login_url='/login/')
def chatNotification(request):
    user = request.user
    friends = user.friends.all()
    arr = []
    for friend in friends:
        chats = ChatMessage.objects.filter(msg_sender__id=friend.profile.id, msg_receiver=user, seen=False)
        arr.append(chats.count())
    return JsonResponse(arr, safe=False)