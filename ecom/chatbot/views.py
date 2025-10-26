from django.shortcuts import render
from django.http import JsonResponse

def chatbot_view(request):
    return render(request, 'chatbot/widget.html', {})

def send_message(request):
    user_message = request.GET.get('message', '')
    bot_reply = "Hello! I'm your virtual mentor 🤖. You said: " + user_message
    return JsonResponse({'response': bot_reply})
