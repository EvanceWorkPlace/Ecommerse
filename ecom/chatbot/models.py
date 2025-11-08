from django.db import models
from django.utils import timezone

class Patient(models.Model):
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=32)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.full_name} ({self.id})"

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    reported_illness = models.TextField(blank=True)
    symptoms = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    consent_given = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Consultation {self.id} for {self.patient}"

class Recommendation(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='recommendations')
    recommended_text = models.TextField(blank=True)   # raw LLM output
    parsed_json = models.JSONField(default=dict)      # structured result parsed from LLM
    clinician_approved = models.BooleanField(default=False)
    escalation = models.BooleanField(default=False)   # whether LLM flagged urgent care
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Recommendation {self.id} (approved={self.clinician_approved})"
