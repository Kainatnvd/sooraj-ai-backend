# from typing import Optional
# from fastapi import APIRouter, Form, UploadFile, File
# from fastapi.responses import JSONResponse, FileResponse
# from app.ai import language, chatbot
# from app.ai.stt import audio_to_text
# from app.ai.tts import text_to_speech
# from dotenv import load_dotenv

# load_dotenv()
# router = APIRouter()

# # -------------------------
# # Text endpoint
# # -------------------------
# @router.post("/text")
# async def chat_text(message: Optional[str] = Form(None)):
#     if not message or not message.strip():
#         # Initial greeting if message is empty
#         return JSONResponse(content={
#             "language": "ur",
#             "reply": "آپ اپنا سوال اردو، انگریزی، یا پنجابی میں لکھ سکتے ہیں۔"
#         })

#     # Detect language
#     user_lang = language.detect_language(message)

#     # Get chatbot reply
#     reply_text = chatbot.get_reply(message, user_lang)

#     return JSONResponse(content={
#         "language": user_lang,
#         "reply": reply_text
#     })

# # -------------------------
# # Voice endpoint
# # -------------------------
# @router.post("/voice")
# async def chat_voice(file: UploadFile = File(...)):
#     try:
#         # 1️⃣ Convert audio → text
#         user_text = await audio_to_text(file)
#         print("STT transcription:", user_text)
#     except Exception as e:
#         print("STT error:", e)
#         return JSONResponse({"error": "Audio transcription failed."}, status_code=500)

#     if not user_text.strip():
#         return JSONResponse({"error": "No speech detected"}, status_code=400)

#     # 2️⃣ Detect language
#     user_lang = language.detect_language(user_text)

#     # 3️⃣ Get chatbot reply
#     reply_text = chatbot.get_reply(user_text, user_lang)

#     # 4️⃣ Return JSON with transcript and reply (no audio for now)
#     return JSONResponse({
#         "text": user_text,
#         "reply": reply_text,
#         "language": user_lang
#     })
from fastapi import APIRouter, Form, UploadFile, File, Query
from fastapi.responses import JSONResponse, FileResponse
from typing import Optional
from urllib.parse import quote
from app.ai import language, chatbot
from app.ai.stt import audio_to_text
from app.ai.tts import text_to_speech
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

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
# Get chatbot reply safely
    reply = chatbot.get_reply(message, user_lang)
    if not reply:
        reply = "معاف کریں، میں ابھی جواب دینے سے قاصر ہوں۔"  # fallback if get_reply fails

    # Return JSON
    return JSONResponse(content={
        "language": user_lang,
        "reply": reply
    })
# @router.post("/voice")
# async def chat_voice(file: UploadFile = File(...)):
#     try:
#         user_text = await audio_to_text(file)
#     except Exception as e:
#         return JSONResponse({"error": "Audio transcription failed."}, status_code=500)

#     if not user_text.strip():
#         return JSONResponse({"error": "No speech detected"}, status_code=400)

#     user_lang = language.detect_language(user_text)
#     reply_text = chatbot.get_reply(user_text, user_lang)

#     return JSONResponse({
#         "text": user_text,
#         "reply": reply_text,
#         "language": user_lang
#     })
# @router.post("/voice")
# async def chat_voice(file: UploadFile = File(...)):
#     try:
#         user_text = await audio_to_text(file)
#     except Exception as e:
#         print("STT ERROR:", e)
#         return JSONResponse({"error": "Audio transcription failed."}, status_code=500)

#     if not user_text.strip():
#         return JSONResponse({"error": "No speech detected"}, status_code=400)

#     # Detect language
#     user_lang = language.detect_language(user_text)

#     # GPT reply
#     reply_text = chatbot.get_reply(user_text, user_lang)

#     # Generate TTS
#     audio_path = text_to_speech(reply_text, user_lang if user_lang != "pa" else "ur")

#     # Return JSON (NOT headers ❌)
#     return JSONResponse({
#         "text": user_text,
#         "reply": reply_text,
#         "language": user_lang,
#         "audio_url": "/api/chat/audio?path=" + quote(audio_path)
#     })
@router.post("/voice")
async def chat_voice(file: UploadFile = File(...)):
    try:
        # 1️⃣ Convert audio → text (Whisper is loaded only in stt.py)
        user_text = await audio_to_text(file)
        print("STT transcription:", user_text)
    except Exception as e:
        print("STT ERROR:", e)
        return JSONResponse({"error": "Audio transcription failed."}, status_code=500)

    if not user_text.strip():
        return JSONResponse({"error": "No speech detected"}, status_code=400)

    # 1️⃣ Detect language
    user_lang = language.detect_language(user_text)

    # 2️⃣ Force Urdu if detected text contains Urdu characters
    if any("\u0600" <= c <= "\u06FF" for c in user_text):  # Arabic script block
        user_lang = "ur"

    # 3️⃣ Get GPT reply
    reply_text = chatbot.get_reply(user_text, user_lang)

    # 4️⃣ Generate TTS (use 'ur' for Urdu, fallback)
    audio_path = text_to_speech(reply_text, user_lang if user_lang != "pa" else "ur")

    # 5️⃣ Return JSON
    return JSONResponse({
        "text": user_text,
        "reply": reply_text,
        "language": user_lang,
        "audio_url": "/api/chat/audio?path=" + quote(audio_path)
    })
@router.get("/audio")
def get_audio(path: str = Query(...)):
    return FileResponse(path, media_type="audio/mpeg")
