from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
import json

from .models import Consultation
from .utils import generate_medicine_recommendation, generate_html_documents_for_consultation


def widget(request):
    return render(request, "chatbot/widget.html")


def chatbot_view(request):
    return render(request, "chatbot/chatbot_view.html")


@csrf_exempt
def chatbot_response(request):
    """Handles chat messages and saves consultation for logged-in users."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    data = json.loads(request.body)
    message = data.get("message", "").strip()

    if not message:
        return JsonResponse({"error": "Message required"}, status=400)

    # AI response
    answer = generate_medicine_recommendation(message)

    consultation_id = None

    # Save consultation if logged in
    if request.user.is_authenticated:
        c = Consultation.objects.create(
            user=request.user,
            question=message,
            answer=answer
        )
        consultation_id = c.id

    return JsonResponse({
        "reply": answer,
        "consultation_id": consultation_id
    })


@login_required
def my_consultations(request):
    qs = Consultation.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "chatbot/my_consultations.html", {"consultations": qs})


@login_required
def consultation_detail(request, pk):
    c = get_object_or_404(Consultation, pk=pk, user=request.user)
    return render(request, "chatbot/consultation_detail.html", {"consultation": c})


# ===============================
# ADMIN DASHBOARD + APPROVAL
# ===============================
@staff_member_required
def admin_dashboard(request):
    """Admin page that shows all consultations."""
    consultations = Consultation.objects.order_by("-created_at")
    return render(request, "chatbot/admin_dashboard.html", {
        "consultations": consultations
    })


@staff_member_required
def approve_consultation(request, pk):
    consult = get_object_or_404(Consultation, id=pk)

    if consult.status != "approved":
        consult.status = "approved"
        consult.approved_by = request.user
        consult.approved_at = timezone.now()

        # Generate HTML documents
        generate_html_documents_for_consultation(consult, email_user=True)

        consult.save()

    return redirect("admin_dashboard")




# ===============================
# VIEW HTML DOCUMENTS
# ===============================
def view_prescription(request, pk):
    consult = get_object_or_404(Consultation, pk=pk)
    return HttpResponse(consult.prescription_html)


def view_sicknote(request, pk):
    consult = get_object_or_404(Consultation, pk=pk)
    return HttpResponse(consult.sicknote_html)


@staff_member_required
def consultation_results(request, pk):
    """
    Admin view to see the generated prescription + sick note
    for an approved consultation.
    """
    consult = get_object_or_404(Consultation, pk=pk)

    return render(request, "chatbot/consultation_results.html", {
        "consultation": consult
    })



@csrf_exempt
def health_analysis(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    disease = data.get("disease")
    blood_sugar = data.get("blood_sugar")
    systolic = data.get("systolic")
    diastolic = data.get("diastolic")
    heart_rate = data.get("heart_rate")
    bmi = data.get("bmi")

    summary = []

    if disease == "diabetes" and blood_sugar:
        sugar = float(blood_sugar)
        if sugar > 180:
            summary.append(f"High blood sugar detected: {sugar}")
        else:
            summary.append(f"Normal blood sugar: {sugar}")

    if disease == "hypertension" and systolic and diastolic:
        sys = float(systolic)
        dia = float(diastolic)
        if sys > 140 or dia > 90:
            summary.append(f"High BP: {sys}/{dia}")
        else:
            summary.append(f"Normal BP: {sys}/{dia}")

    if disease == "cardiac" and heart_rate:
        hr = float(heart_rate)
        if hr > 100:
            summary.append(f"High HR: {hr}")
        else:
            summary.append(f"Normal HR: {hr}")

    if bmi:
        b = float(bmi)
        if b > 30:
            summary.append(f"Obesity (BMI {b})")
        elif b < 18.5:
            summary.append(f"Underweight (BMI {b})")
        else:
            summary.append(f"Healthy BMI {b}")

    question = f"""
    Disease: {disease}
    Blood Sugar: {blood_sugar}
    BP: {systolic}/{diastolic}
    Heart Rate: {heart_rate}
    BMI: {bmi}
    """

    ai_feedback = generate_medicine_recommendation(question)

    return JsonResponse({
        "summary": summary,
        "ai_feedback": ai_feedback
    })

