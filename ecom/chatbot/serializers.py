from rest_framework import serializers
from .models import Patient, Consultation, Recommendation

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id','full_name','date_of_birth','gender','created_at']

class ConsultationSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()

    class Meta:
        model = Consultation
        fields = ['id','patient','reported_illness','symptoms','allergies','current_medications','consent_given','completed','created_at']

    def create(self, validated_data):
        patient_data = validated_data.pop('patient')
        patient, _ = Patient.objects.get_or_create(
            full_name=patient_data['full_name'],
            date_of_birth=patient_data['date_of_birth'],
            gender=patient_data.get('gender','')
        )
        cons = Consultation.objects.create(patient=patient, **validated_data)
        return cons

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ['id','consultation','recommended_text','parsed_json','clinician_approved','escalation','created_at']
        read_only_fields = ['recommended_text','parsed_json','created_at','escalation']
