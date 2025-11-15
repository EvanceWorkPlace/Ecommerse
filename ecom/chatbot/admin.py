from django.contrib import admin
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import Consultation, HealthRecord

@admin.action(description="Approve selected consultations and generate HTML docs")
def approve_and_generate(modeladmin, request, queryset):
    for c in queryset.filter(status='pending'):
        c.status = 'approved'
        c.approved_by = request.user
        c.approved_at = timezone.now()

        # Render HTML templates (strings)
        ctx = {'user': c.user, 'consultation': c, 'question': c.question, 'answer': c.answer}
        pres_html = render_to_string('chatbot/prescription_template.html', ctx)
        sick_html = render_to_string('chatbot/sicknote_template.html', ctx)

        c.prescription_html = pres_html
        c.sicknote_html = sick_html

        # Optionally email the user with HTML docs
        try:
            if getattr(c.user, 'email', None):
                mail = EmailMessage(
                    subject=f"Your documents for consultation #{c.pk}",
                    body="Please find your documents below.",
                    to=[c.user.email],
                )
                # Attach HTML in email body (or as separate HTML attachments)
                # Here we include both documents' HTML in the email body (simple approach)
                html_body = f"<h2>Prescription</h2>{pres_html}<hr><h2>Sick Note</h2>{sick_html}"
                mail.content_subtype = "html"
                mail.body = html_body
                mail.send(fail_silently=True)
        except Exception:
            # don't break admin action if email fails
            pass

        c.save()


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'status', 'created_at', 'approved_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email', 'question')
    actions = [approve_and_generate]


# Keep HealthRecord admin if you like
@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('disease', 'blood_sugar', 'blood_pressure_sys', 'blood_pressure_dia', 'heart_rate', 'bmi', 'created_at')
    list_filter = ('disease',)
    readonly_fields = ('created_at',)
