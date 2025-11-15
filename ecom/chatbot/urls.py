
from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chatbot_view, name="chatbot_view"),
    path('chatbot_response/', views.chatbot_response, name="chatbot_response"),

    path('widget/', views.widget, name="widget"),
    path('health_analysis/', views.health_analysis, name='health_analysis'),
    # User consultations
    path('consultations/', views.my_consultations, name="my_consultations"),
    path('consultations/<int:pk>/', views.consultation_detail, name="consultation_detail"),

    # Admin dashboard
    path('admin/consultations/', views.admin_dashboard, name="admin_dashboard"),
    path('admin/consultations/<int:pk>/approve/', views.approve_consultation, name="approve_consultation"),
    path("consultation/<int:pk>/results/", views.consultation_results, name="consultation_results"),

    # View documents
    path("consultation/<int:pk>/prescription/", views.view_prescription, name="view_prescription"),
    path("consultation/<int:pk>/sicknote/", views.view_sicknote, name="view_sicknote"),
]
