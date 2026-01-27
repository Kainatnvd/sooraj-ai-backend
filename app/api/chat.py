from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from app.ai import chatbot, language, tts

router = APIRouter()

# Simple hello endpoint
@router.get("/hello")
async def say_hello():
    return {"message": "Hello from Sooraj AI Backend!"}

# Text chatbot endpoint
@router.post("/text")
async def chat_text(message: str = Form(...), lang: str = Form("ur")):
    """
    lang: "ur" for Urdu (default), "pa" for Punjabi, "en" for English
    """
    # Step 1: Detect language if not provided
    user_lang = lang or language.detect_language(message)
    
    # Step 2: Get AI reply from chatbot.py
    reply_text = chatbot.get_reply(message, language=user_lang)
    
    # Step 3: Convert to audio
    audio_file = tts.text_to_speech(reply_text, lang=user_lang)
    
    return JSONResponse(content={
        "reply": reply_text,
        "audio_file": audio_file
    })

# Voice chatbot endpoint (placeholder)
@router.post("/voice")
async def chat_voice_placeholder():
    return JSONResponse(content={
        "message": "Voice chatbot functionality coming soon."
    })
