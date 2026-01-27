from langdetect import detect

def detect_language(text: str) -> str:
    try:
        lang = detect(text)
    except:
        lang = "en"
    return lang

