from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import os
from .utils import generate_medicine_recommendation

def widget(request):
    return render(request, 'chatbot/widget.html', {})

def chatbot_view(request):
    return render(request, 'chatbot/chatbot_view.html', {})

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get('message', '')
        response = generate_medicine_recommendation(user_input)
        return JsonResponse({'reply': response['response']})
    return JsonResponse({'error': 'Invalid request method'}, status=400)









