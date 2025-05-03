from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import json
import os
from django.conf import settings
from django.http import JsonResponse

def Home(request):
    return render(request, "chatapp/home.html")


def UserRegister(request):
    if request.method == 'POST':
        Username = request.POST['username']
        Email = request.POST['email']
        Password = request.POST['password']
        Password2 = request.POST['password2']
       
        if User.objects.filter(Email=Email).exists():
            messages.error(request, "User already exists!")
            return redirect('register')
        elif User.objects.filter(Username=Username).exists():
            messages.error(request, "User already exists!")
            return redirect('register')
        else:
            if Password == Password2:
                newuser = User.objects.create(Username=Username, Email=Email, Password=Password)
                request.session['Username'] = newuser.Username
                request.session['Email'] = newuser.Email
                return redirect('search_user')
            else:
                messages.error(request, "Passwords don't match!")
                return render(request, 'chatapp/signup.html')
    return render(request, 'chatapp/signup.html')

# login page views

def LoginUser(request):
    if request.method == "POST":
        Email = request.POST['email']
        Password = request.POST['password']

        try:
            user = User.objects.get(Email=Email)
            if user.Password == Password:
                request.session['Username'] = user.Username
                request.session['Email'] = user.Email
                return redirect("search_user")
            else:
                messages.error(request, "Wrong password!")
        except User.DoesNotExist:
            messages.error(request, "User does not exist!")

    return render(request, 'chatapp/login.html')  

# STARTING CHAT LOGIC

def SearchUser(request):
    if 'Email' not in request.session:
        messages.error(request, "You need to login first")
        return redirect('login')
    query = request.GET.get('q')
    searched_user = None
    searched = False

    if query:
        try:
            searched_user = User.objects.get(Username=query)
        except User.DoesNotExist:
            searched_user = None
        searched = True

    return render(request, 'chatapp/search.html', {
        'searched_user': searched_user,
        'searched': searched
    })

def ChatView(request, user_id):
    if 'Username' not in request.session:
        return redirect('login')

    try:
        receiver = User.objects.get(id=user_id)
        sender_username = request.session['Username']
        receiver_username = receiver.Username
    except User.DoesNotExist:
        messages.error(request, "User does not exist.")
        return redirect('search_user')

    chat_log_path = os.path.join(settings.BASE_DIR, 'chat_log.json')

    if not os.path.exists(chat_log_path):
        with open(chat_log_path, 'w') as f:
            json.dump([], f)

    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print("POST Request received")
        message = request.POST.get("message")
        if message.strip() != "":
            with open(chat_log_path, 'r+') as f:
                data = json.load(f)
                data.append({
                    "sender": sender_username,
                    "receiver": receiver_username,
                    "message": message
                })
                f.seek(0)
                json.dump(data, f, indent=2)
        return JsonResponse({"status": "success"})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        print("GET Request received for messages")
        with open(chat_log_path, 'r') as f:
            all_messages = json.load(f)

        conversation = [
            msg for msg in all_messages
            if (msg['sender'] == sender_username and msg['receiver'] == receiver_username) or
               (msg['sender'] == receiver_username and msg['receiver'] == sender_username)
        ]
        print(f"Returning conversation: {conversation}")
        return JsonResponse({"messages": conversation})

    with open(chat_log_path, 'r') as f:
        all_messages = json.load(f)

    conversation = [
        msg for msg in all_messages
        if (msg['sender'] == sender_username and msg['receiver'] == receiver_username) or
           (msg['sender'] == receiver_username and msg['receiver'] == sender_username)
    ]

    return render(request, 'chatapp/chat.html', {
        'receiver': receiver,
        'messages': conversation,
    })