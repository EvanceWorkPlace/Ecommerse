from django.db import models

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

