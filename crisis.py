from typing import List

# List of keywords that might indicate a crisis or suicidal ideation
CRISIS_KEYWORDS: List[str] = [
    "suicidal", "suicide", "kill myself", "want to die", "hopeless",
    "worthless", "can't go on", "give up", "ending it all", "no reason to live",
    "end my life", "hurt myself", "self harm"
]

# A compassionate safety message to show instead of a chatbot reply
SAFETY_MESSAGE = (
    "It sounds like you’re going through a really tough time. "
    "You’re not alone, and there are people who want to help you.\n\n"
    "If you are in immediate danger, please reach out to someone you trust or contact a professional:\n\n"
    "🇮🇳 **India Helplines:**\n"
    "iCall: +91 9152987821\n"
    "Vandrevala Foundation Helpline: 1800-599-0019\n\n"
    "If you’re outside India, please look for local helplines at: https://findahelpline.com\n"
)

def contains_crisis_keywords(text: str) -> bool:
    """
    Checks if the input text contains any crisis-related keywords.
    Returns True if a match is found.
    """
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>crisis function called ")
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in CRISIS_KEYWORDS)

def get_crisis_message() -> str:
    """
    Returns a safe message to display when a crisis keyword is detected.
    """
    return SAFETY_MESSAGE
