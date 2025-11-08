from django.urls import path
from . import views

urlpatterns = [
    path('widget/', views.widget, name='widget'),
    path('start/', views.start_consultation, name='start_consultation'),
    path('consultation/<int:consultation_id>/answers/', views.add_answers, name='add_answers'),
    path('consultation/<int:consultation_id>/recommend/', views.generate_recommendation, name='generate_recommendation'),
    path('recommendation/<int:recommendation_id>/', views.get_recommendation, name='get_recommendation'),
]
