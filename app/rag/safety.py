EMERGENCY_KEYWORDS = [
    "chest pain",
    "suicide",
    "severe bleeding",
    "heart attack",
]

EMERGENCY_RESPONSE = "This may be a medical emergency. Please seek immediate medical help."

def detect_emergency(query: str) -> bool:
    """
    Checks if the user's query contains any emergency keywords.
    """
    query_lower = query.lower()
    for keyword in EMERGENCY_KEYWORDS:
        if keyword in query_lower:
            return True
    return False
