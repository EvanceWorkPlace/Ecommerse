# chatbot/context_processors.py
from .models import Consultation

def pending_consultations_count(request):
    """
    Adds `pending_consultations_count` to template context for staff users.
    """
    if request.user.is_authenticated and request.user.is_staff:
        count = Consultation.objects.filter(approved=False).count()
    else:
        count = 0
    return {"pending_consultations_count": count}
