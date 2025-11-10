from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .utils import generate_medicine_recommendation
from .models import HealthRecord




def widget(request):
    return render(request, 'chatbot/widget.html', {})

def chatbot_view(request):
    return render(request, 'chatbot/chatbot_view.html', {})

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get('message', '')
        response = generate_medicine_recommendation(user_input)
        return JsonResponse({'reply': response['response']})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def health_analysis(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        disease = data.get('disease')
        blood_sugar = float(data.get('blood_sugar', 0))
        systolic = float(data.get('systolic', 0))
        diastolic = float(data.get('diastolic', 0))
        heart_rate = float(data.get('heart_rate', 0))
        bmi = float(data.get('bmi', 0))

        # Save to DB
        HealthRecord.objects.create(
            disease=disease,
            blood_sugar=blood_sugar,
            blood_pressure_sys=systolic,
            blood_pressure_dia=diastolic,
            heart_rate=heart_rate,
            bmi=bmi,
        )

        # Simple analysis logic
        result = []
        if disease == 'diabetes':
            if blood_sugar > 180:
                result.append("⚠️ High blood sugar detected.")
            elif blood_sugar < 70:
                result.append("⚠️ Low blood sugar detected.")
            else:
                result.append("✅ Blood sugar is in normal range.")

        if disease == 'hypertension':
            if systolic > 140 or diastolic > 90:
                result.append("⚠️ Blood pressure is high.")
            elif systolic < 90 or diastolic < 60:
                result.append("⚠️ Blood pressure is low.")
            else:
                result.append("✅ Blood pressure looks stable.")

        if disease == 'cardiac':
            if heart_rate > 100:
                result.append("⚠️ Elevated heart rate detected.")
            elif heart_rate < 50:
                result.append("⚠️ Low heart rate detected.")
            else:
                result.append("✅ Heart rate is normal.")

        # Generate AI-based recommendation
        prompt = f"""
        A patient with {disease} entered the following data:
        Blood sugar: {blood_sugar}, BP: {systolic}/{diastolic}, HR: {heart_rate}, BMI: {bmi}.
        Provide personalized, safe health advice in 3 concise bullet points.
        """
        ai_feedback = generate_medicine_recommendation(prompt)

        return JsonResponse({
            "summary": result,
            "ai_feedback": ai_feedback['response']
        })

    return JsonResponse({'error': 'Invalid request method'}, status=400)





