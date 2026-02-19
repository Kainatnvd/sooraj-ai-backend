# import whisper
# import os
# import tempfile
# from fastapi import UploadFile

# # Load Whisper model ONCE at startup
# model = whisper.load_model("small")  # or "base", "medium"

# async def audio_to_text(file: UploadFile) -> str:
#     """
#     Async-safe speech-to-text using Whisper.
#     Works with any audio format supported by ffmpeg.
#     """

#     # 1️⃣ Read audio bytes asynchronously (CRITICAL FIX)
#     audio_bytes = await file.read()

#     # 2️⃣ Preserve original extension (important for ffmpeg)
#     _, ext = os.path.splitext(file.filename)
#     if not ext:
#         ext = ".wav"  # fallback

#     # 3️⃣ Write to a temp file
#     with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
#         tmp.write(audio_bytes)
#         tmp_path = tmp.name

#     try:
#         # 4️⃣ Transcribe
#         result = model.transcribe(tmp_path)
#         text = result.get("text", "").strip()
#         return text

#     finally:
#         # 5️⃣ Cleanup (always runs)
#         os.remove(tmp_path)
import whisper
import os
import tempfile
from fastapi import UploadFile

model = None

def get_model():
    global model
    if model is None:
        model = whisper.load_model("small")
    return model

async def audio_to_text(file: UploadFile) -> str:
    audio_bytes = await file.read()

    _, ext = os.path.splitext(file.filename)
    if not ext:
        ext = ".wav"

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        m = get_model()
        result = m.transcribe(tmp_path)
        return result.get("text", "").strip()

    finally:
        os.remove(tmp_path)
