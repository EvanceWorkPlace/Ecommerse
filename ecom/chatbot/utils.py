import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_medicine_recommendation(prompt: str):
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(
            f"You are a helpful medical assistant. Based on the user's symptoms, recommend safe over-the-counter medicines.\n\nUser: {prompt}"
        )
        return {"response": response.text}

    except Exception as e:
        return {"response": f"⚠️ Error using Gemini API: {str(e)}"}