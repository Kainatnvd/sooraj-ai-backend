from typing import Optional
from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from app.ai import language, chatbot

router = APIRouter()

@router.get("/hello")
async def say_hello():
    return {"message": "Hello from Sooraj AI Backend!"}

@router.post("/text")
async def chat_text(message: Optional[str] = Form(None)):
      # 🟢 Initial greeting (when chat opens)
    if not message.strip():
        return JSONResponse(content={
            "language": "ur",
            "reply": "آپ اپنا سوال اردو، انگریزی، یا پنجابی میں لکھ سکتے ہیں۔"
        })
    
    # 1️⃣ Detect language
    user_lang = language.detect_language(message)

    # 2️⃣ Get chatbot reply (NO RAG)
    reply_text = chatbot.get_reply(message, user_lang)

    return JSONResponse(content={
        "language": user_lang,
        "reply": reply_text
    })


# Voice chatbot endpoint (placeholder)
@router.post("/voice")
async def chat_voice_placeholder():
    return JSONResponse(content={
        "message": "Voice chatbot functionality coming soon."
    })
