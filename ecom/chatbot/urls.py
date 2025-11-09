from django.urls import path
from . import views

urlpatterns = [
    path('chatbot_view/',views.chatbot_view, name='chatbot_view'),
    path('widget/', views.widget, name='widget'),
    path('chatbot_response/', views.chatbot_response, name='chatbot_response'),
    
]
