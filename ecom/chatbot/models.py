from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User




# Keep your existing HealthRecord model
class HealthRecord(models.Model):
    DISEASE_CHOICES = [
        ('diabetes', 'Diabetes'),
        ('hypertension', 'Hypertension'),
        ('cardiac', 'Heart Disease'),
    ]

    disease = models.CharField(max_length=50, choices=DISEASE_CHOICES)
    blood_sugar = models.FloatField(null=True, blank=True)
    blood_pressure_sys = models.FloatField(null=True, blank=True)
    blood_pressure_dia = models.FloatField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)
    bmi = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.disease} Record ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


# New Consultation model for chat-based requests and document generation (HTML)
# chatbot/models.py
class Consultation(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    question = models.TextField()
    answer = models.TextField(blank=True, null=True)

    # Admin approval system
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    approved_at = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_consultations"
    )

    # HTML documents
    prescription_html = models.TextField(blank=True, null=True)
    sicknote_html = models.TextField(blank=True, null=True)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consultation #{self.pk} for {self.user.username}"
