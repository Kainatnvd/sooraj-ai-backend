from typing import Optional
from fastapi import APIRouter, Form, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
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
        # 1️⃣ Convert audio → text
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

    # 4️⃣ Return JSON with transcript and reply (no audio for now)
    return JSONResponse({
        "text": user_text,
        "reply": reply_text,
        "language": user_lang
    })
