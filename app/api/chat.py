from typing import Optional
from fastapi import APIRouter, Form, UploadFile, File
from fastapi.responses import JSONResponse
from app.ai import language, chatbot
from app.ai.stt import audio_to_text
from app.ai.tts import text_to_speech
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

# -------------------------
# Text endpoint
# -------------------------
@router.post("/text")
async def chat_text(message: Optional[str] = Form(None)):
    if not message or not message.strip():
        # Initial greeting if message is empty
        return JSONResponse(content={
            "language": "ur",
            "reply": "آپ اپنا سوال اردو، انگریزی، یا پنجابی میں لکھ سکتے ہیں۔"
        })

    # Detect language
    user_lang = language.detect_language(message)

    # Get chatbot reply
    reply_text = chatbot.get_reply(message, user_lang)
    return JSONResponse({"language": user_lang, "reply": reply_text})

    return JSONResponse(content={
        "language": user_lang,
        "reply": reply_text
    })

# -------------------------
# Voice endpoint
# -------------------------
@router.post("/voice")
async def chat_voice(file: UploadFile = File(...)):
    try:
        # 1️⃣ Convert audio → text (Whisper is loaded only in stt.py)
        user_text = await audio_to_text(file)
        print("STT transcription:", user_text)
    except Exception as e:
        print("STT error:", e)
        return JSONResponse({"error": "Audio transcription failed."}, status_code=500)

    if not user_text.strip():
        return JSONResponse({"error": "No speech detected"}, status_code=400)

    # 2️⃣ Detect language
    user_lang = language.detect_language(user_text)

    # 3️⃣ Get chatbot reply
    reply_text = chatbot.get_reply(user_text, user_lang)

    try:
        # 4️⃣ Convert reply → audio (safe TTS language)
        tts_lang = "ur" if user_lang in ["ur", "pa"] else "en"
        audio_path = text_to_speech(reply_text, lang=tts_lang)
    except Exception as e:
        print("TTS error:", e)
        return JSONResponse({"error": "TTS failed"}, status_code=500)

    # 5️⃣ Return audio with transcript in headers
    return FileResponse(
        audio_path,
        media_type="audio/mpeg",
        headers={"X-Transcript": user_text}
    )
