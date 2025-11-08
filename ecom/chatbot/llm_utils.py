import json
import re
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser



# Configure the LLM (using OpenAI-compatible API key)
def get_llm():
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)


PROMPT_TEMPLATE = """
SYSTEM: You are a conservative clinical decision-support assistant. ONLY provide suggestions meant for clinician review.
Do NOT create legally binding prescriptions. If the patient's presentation suggests urgent care (chest pain, severe shortness of breath, seizures, severe bleeding, high fever in infants, altered mental status), set "escalation": true and explain why.

USER PATIENT:
Name: {name}
DOB: {dob}
Gender: {gender}
Reported illness: {illness}
Symptoms: {symptoms}
Allergies: {allergies}
Current medications: {current_meds}

Task:
1) Provide up to 3 suggestions (prefer OTC or symptomatic care) and for each suggestion include:
   - name
   - typical_dose (string)
   - otc (true/false)
   - contraindications (short string)
   - notes (short string)
2) Provide a short "rationale" string.
3) Provide "escalation": true|false
Return only valid JSON with keys: suggestions (list), escalation (bool), rationale (string).
Ensure dose numbers are numeric where relevant and include units (mg, mL, etc). Example output:

{
 "suggestions": [
   {"name":"Paracetamol", "typical_dose":"500-1000 mg every 4-6h (max 4000 mg/day)", "otc": true, "contraindications":"Severe liver disease", "notes":"Avoid with alcohol"}
 ],
 "escalation": false,
 "rationale": "Based on symptoms X..."
}
"""

# Create chat prompt template
PROMPT = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)


def call_llm_and_parse(patient_data: Dict[str, Any], context: str = "") -> Dict[str, Any]:
    llm = get_llm()

    # Inject retrieved context into prompt
    prompt_with_context = PROMPT_TEMPLATE + f"\n\nRETRIEVED CONTEXT:\n{context}\n\nUse this context to inform your suggestions."

    prompt = ChatPromptTemplate.from_template(prompt_with_context)
    chain = prompt | llm | StrOutputParser()
    raw = chain.invoke(patient_data)

    json_text = extract_json(raw)
    if not json_text:
        return {"raw": raw, "parse_error": True}
    try:
        parsed = json.loads(json_text)
    except Exception as e:
        return {"raw": raw, "parse_error": True, "error": str(e)}
    return {"raw": raw, "parsed": parsed}


def extract_json(text: str) -> str:
    """
    Attempts to find a JSON object in text and return it.
    """
    text_clean = re.sub(r"```(?:json)?", "", text)
    start = text_clean.find('{')
    if start == -1:
        return ""
    depth = 0
    for i in range(start, len(text_clean)):
        if text_clean[i] == '{':
            depth += 1
        elif text_clean[i] == '}':
            depth -= 1
            if depth == 0:
                return text_clean[start:i+1].strip()
    return ""
