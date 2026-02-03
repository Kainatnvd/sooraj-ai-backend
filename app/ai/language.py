# app/ai/language.py
from langdetect import detect

PUNJABI_HINTS = {"تے", "وچ", "ایہ", "اوہ", "نیں", "ساڈا", "تہاڈا", "کیوں", "ہن"}

def detect_language(text: str) -> str:
    text = text.strip()
    if not text:
        return "ur"
    # Shahmukhi Punjabi heuristic
    for word in PUNJABI_HINTS:
        if word in text:
            return "pa"
    try:
        lang = detect(text)
        if lang == "ur":
            return "ur"
        elif lang == "en":
            return "en"
        else:
            return "en"
    except:
        return "en"
