import google.generativeai as genai
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


# =============================================
# 1. GEMINI AI — Generate Medical Recommendation
# =============================================
def generate_medicine_recommendation(question):

    api_key = getattr(settings, "GEMINI_API_KEY", None)

    if not api_key:
        return "Gemini API key missing. Please set GEMINI_API_KEY in settings.py"

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(
            f"""
            You are a medical assistant. Provide safe, clear guidance.
            Do NOT diagnose conditions.
            Only recommend OTC medication when safe.
            Advise when to seek a doctor.

            User question: {question}
            """
        )

        return response.text or "No response."

    except Exception as e:
        return f"AI Error (Gemini): {str(e)}"



# ========================================================
# 2. Generate HTML Prescription + Sick Note (No PDF)
# ========================================================
def generate_html_documents_for_consultation(consultation, email_user=True):
    """
    Creates:
    - consultation.prescription_html
    - consultation.sicknote_html
    And optionally emails them to the user.
    """

    context = {
        "user": consultation.user,
        "consultation": consultation,
        "question": consultation.question,
        "answer": consultation.answer,
    }

    # -------------------------
    # Render HTML Templates
    # -------------------------
    pres_html = render_to_string("chatbot/prescription_template.html", context)
    sick_html = render_to_string("chatbot/sicknote_template.html", context)

    # Save HTML into DB
    consultation.prescription_html = pres_html
    consultation.sicknote_html = sick_html
    consultation.save()

    # -------------------------
    # Optional Email Delivery
    # -------------------------
    if email_user and getattr(consultation.user, "email", None):
        try:
            email = EmailMessage(
                subject=f"Your Consultation Documents #{consultation.pk}",
                body=(
                    "<h2>Your Prescription</h2>"
                    + pres_html +
                    "<hr>"
                    "<h2>Your Sick Note</h2>"
                    + sick_html
                ),
                to=[consultation.user.email],
            )
            email.content_subtype = "html"
            email.send(fail_silently=True)
        except Exception:
            pass

    return pres_html, sick_html
