# from typing import Optional
# from fastapi import APIRouter, Form
# from fastapi.responses import JSONResponse
# from app.ai import language, chatbot
# import whisper
# from gtts import gTTS
# from fastapi import UploadFile, File
# from fastapi.responses import FileResponse


# router = APIRouter()

# @router.get("/hello")
# async def say_hello():
#     return {"message": "Hello from Sooraj AI Backend!"}

# @router.post("/text")
# async def chat_text(message: Optional[str] = Form(None)):
#       # 🟢 Initial greeting (when chat opens)
#     if not message.strip():
#         return JSONResponse(content={
#             "language": "ur",
#             "reply": "آپ اپنا سوال اردو، انگریزی، یا پنجابی میں لکھ سکتے ہیں۔"
#         })
    
#     # 1️⃣ Detect language
#     user_lang = language.detect_language(message)

#     # 2️⃣ Get chatbot reply (NO RAG)
#     reply_text = chatbot.get_reply(message, user_lang)

#     return JSONResponse(content={
#         "language": user_lang,
#         "reply": reply_text
#     })


# # Voice chatbot endpoint (placeholder)
# whisper_model = whisper.load_model("small")  # tiny, base, small, medium, large


# @router.post("/voice")
# async def chat_voice(file: UploadFile = File(...)):
#     """
#     Receive audio from frontend → transcribe → detect language → get chatbot reply → return TTS audio + transcript
#     """
#     # 1️⃣ Save uploaded audio temporarily
#     temp_audio_path = "temp_input.wav"
#     temp_reply_path = "temp_reply.mp3"
    
#     audio_bytes = await file.read()
#     with open(temp_audio_path, "wb") as f:
#         f.write(audio_bytes)

#     # 2️⃣ Transcribe audio → text
#     try:
#         result = whisper_model.transcribe(temp_audio_path)
#         user_text = result["text"].strip()
#     except Exception as e:
#         print("STT error:", e)
#         return {"error": "Audio transcription failed."}

#     if not user_text:
#         user_text = ""  # optional: send default message

#     # 3️⃣ Detect language
#     user_lang = language.detect_language(user_text)

#     # 4️⃣ Get chatbot reply
#     reply_text = chatbot.get_reply(user_text, user_lang)

#     # 5️⃣ Convert reply → audio (TTS)
#     try:
#         tts = gTTS(text=reply_text, lang=user_lang)
#         tts.save(temp_reply_path)
#     except Exception as e:
#         print("TTS error:", e)
#         return {"error": "Text-to-speech failed."}

#     # 6️⃣ Return audio file **with transcript in headers**
#     return FileResponse(
#         temp_reply_path,
#         media_type="audio/mpeg",
#         headers={"X-Transcript": user_text}  # <-- send transcription
#     )

# chat.py
from typing import Optional
from fastapi import APIRouter, Form, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from app.ai import language, chatbot
# import whisper
# from gtts import gTTS
from dotenv import load_dotenv
load_dotenv()
router = APIRouter()

# Text endpoint
@router.post("/text")
async def chat_text(message: Optional[str] = Form(None)):
    if not message or not message.strip():
        return JSONResponse(content={
            "language": "ur",
            "reply": "آپ اپنا سوال اردو، انگریزی، یا پنجابی میں لکھ سکتے ہیں۔"
        })
    
    user_lang = language.detect_language(message)
    reply_text = chatbot.get_reply(message, user_lang)

    return JSONResponse(content={
        "language": user_lang,
        "reply": reply_text
    })

# # Load Whisper model once
# whisper_model = whisper.load_model("small")

# # Voice endpoint
# @router.post("/voice")
# async def chat_voice(file: UploadFile = File(...)):
#     temp_audio_path = "temp_input.webm"
#     temp_reply_path = "temp_reply.mp3"

#     # Save uploaded audio
#     audio_bytes = await file.read()
#     with open(temp_audio_path, "wb") as f:
#         f.write(audio_bytes)

#     # Transcribe using Whisper
#     try:
#         result = whisper_model.transcribe(temp_audio_path)
#         user_text = result.get("text", "").strip()
#         print("Whisper transcription:", user_text)
#     except Exception as e:
#         print("STT error:", e)
#         return JSONResponse({"error": "Transcription failed."}, status_code=500)

#     if not user_text:
#         user_text = "🎤"

#     # Detect language
#     user_lang = language.detect_language(user_text)

#     # Get chatbot reply
#     reply_text = chatbot.get_reply(user_text, user_lang)

#     # Convert reply to audio
#     try:
#         tts_lang = "ur" if user_lang == "ur" else "en"
#         tts = gTTS(text=reply_text, lang=tts_lang)
#         tts.save(temp_reply_path)
#     except Exception as e:
#         print("TTS error:", e)
#         return JSONResponse({"error": "TTS failed"}, status_code=500)

#     return FileResponse(
#         temp_reply_path,
#         media_type="audio/mpeg",
#         headers={"X-Transcript": user_text}
#     )
    