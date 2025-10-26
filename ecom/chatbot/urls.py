from django.urls import path
from . import views

urlpatterns = [
    path('chatbot_view/', views.chatbot_view, name='chatbot_view'),
    path('send_message/', views.send_message, name='send_message'),
]