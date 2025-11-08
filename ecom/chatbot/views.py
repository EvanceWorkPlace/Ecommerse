from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Consultation, Recommendation
from .serializers import ConsultationSerializer, RecommendationSerializer
from .llm_utils import call_llm_and_parse
from .safety_checks import contains_red_flag, dose_sanity_check
from django.shortcuts import render, redirect

@api_view(['POST'])
@permission_classes([AllowAny])
def start_consultation(request):
    """
    Create patient + consultation. Expected payload:
    {
      "patient": {"full_name":"...", "date_of_birth":"YYYY-MM-DD", "gender":"..."},
      "reported_illness":"...", "symptoms":"...", "allergies":"", "current_medications":"", "consent_given":true
    }
    """
    serializer = ConsultationSerializer(data=request.data)
    if serializer.is_valid():
        cons = serializer.save()
        return Response(ConsultationSerializer(cons).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def add_answers(request, consultation_id):
    """
    Update the consultation with more details (symptoms etc).
    """
    cons = get_object_or_404(Consultation, pk=consultation_id)
    for fld in ['reported_illness','symptoms','allergies','current_medications','consent_given','completed']:
        if fld in request.data:
            setattr(cons, fld, request.data[fld])
    cons.save()
    return Response(ConsultationSerializer(cons).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # only authenticated users can generate calls
def generate_recommendation(request, consultation_id):
    cons = get_object_or_404(Consultation, pk=consultation_id)
    if not cons.consent_given:
        return Response({"detail":"Consent required to proceed."}, status=status.HTTP_400_BAD_REQUEST)

    patient_data = {
        "name": cons.patient.full_name,
        "dob": cons.patient.date_of_birth.isoformat(),
        "gender": cons.patient.gender,
        "illness": cons.reported_illness or "",
        "symptoms": cons.symptoms or "",
        "allergies": cons.allergies or "",
        "current_meds": cons.current_medications or "",
    }
    llm_result = call_llm_and_parse(patient_data)
    # default parsed
    parsed = llm_result.get('parsed') or {}
    escalation_flag = parsed.get('escalation', False) if isinstance(parsed, dict) else False

    # safety checks
    issues = []
    if contains_red_flag(cons.symptoms or ""):
        escalation_flag = True
        issues.append("Detected red-flag symptoms — escalate to clinician.")

    suggestions = parsed.get('suggestions', []) if isinstance(parsed, dict) else []
    dose_issues = dose_sanity_check(suggestions)
    issues.extend(dose_issues)
    if dose_issues:
        escalation_flag = True

    rec = Recommendation.objects.create(
        consultation=cons,
        recommended_text=llm_result.get('raw', ''),
        parsed_json=parsed if isinstance(parsed, dict) else {},
        escalation=escalation_flag
    )

    # Respond with rec id and issues for UI
    return Response({
        "recommendation_id": rec.id,
        "escalation": rec.escalation,
        "issues": issues,
        "raw_text": llm_result.get('raw','')
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendation(request, recommendation_id):
    rec = get_object_or_404(Recommendation, pk=recommendation_id)
    return Response(RecommendationSerializer(rec).data)


def widget(request):
    return render(request, 'chatbot/widget.html', {})

