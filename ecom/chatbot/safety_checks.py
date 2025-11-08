from typing import Dict, Any
import re

# A minimal set of red-flag keywords (extend as needed)
RED_FLAGS = [
    'chest pain','shortness of breath','severe bleeding','loss of consciousness',
    'seizure','sudden weakness','sudden numbness','high fever','confusion'
]

# Example dose sanity ranges for a few common meds (simplified)
DOSE_RANGES = {
    'paracetamol': {'min_mg': 250, 'max_mg': 4000}, # per day max use with caution
    'ibuprofen': {'min_mg': 200, 'max_mg': 2400},
}

def contains_red_flag(symptoms_text: str) -> bool:
    txt = symptoms_text.lower()
    return any(flag in txt for flag in RED_FLAGS)

def normalize_med_name(name: str) -> str:
    return re.sub(r'[^a-z0-9 ]','',name.lower()).strip()

def dose_sanity_check(suggestions: list) -> list:
    """
    Returns list of issues found. For each suggestion check if dose falls within naive ranges.
    This is a heuristic check only.
    """
    issues = []
    for s in suggestions:
        name_norm = normalize_med_name(s.get('name',''))
        if name_norm in DOSE_RANGES:
            typical = s.get('typical_dose','')
            # find numbers in typical dose
            nums = [int(n) for n in re.findall(r'(\d{2,5})', typical)]
            if nums:
                # we check the largest number against max_mg
                max_in_text = max(nums)
                max_allowed = DOSE_RANGES[name_norm]['max_mg']
                if max_in_text > max_allowed:
                    issues.append(f"{s.get('name')} dose seems above allowed max ({max_in_text} > {max_allowed})")
    return issues
