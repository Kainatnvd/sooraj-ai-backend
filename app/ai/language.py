from langdetect import detect

# Common Punjabi words written in Shahmukhi
PUNJABI_HINTS = {
    "تے", "وچ", "ایہ", "اوہ", "نیں", "ساڈا", "تہاڈا", "کیوں", "ہن"
}

def detect_language(text: str) -> str:
    text = text.strip()

    # Empty message → default Urdu greeting
    if not text:
        return "ur"

    # Punjabi heuristic (Shahmukhi)
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
            return "en"   # ✅ IMPORTANT FIX

    except Exception as e:
        print("Language detection error:", e)
        return "en"       # ✅ IMPORTANT FIX
