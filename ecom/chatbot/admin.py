from django.contrib import admin
from .models import Patient, Consultation, Recommendation

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id','full_name','date_of_birth','gender','created_at')
    search_fields = ('full_name',)

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('id','patient','reported_illness','consent_given','completed','created_at')
    list_filter = ('consent_given','completed')
    search_fields = ('patient__full_name','reported_illness')

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('id','consultation','clinician_approved','escalation','created_at')
    actions = ['approve_recommendations']

    def approve_recommendations(self, request, queryset):
        updated = queryset.update(clinician_approved=True)
        self.message_user(request, f"{updated} recommendations approved.")
    approve_recommendations.short_description = "Mark selected recommendations as clinician_approved"
