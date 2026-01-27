# import whisper
# from fastapi import UploadFile

# # Load Whisper model once
# model = whisper.load_model("base")  # you can use "small" for faster processing

# def audio_to_text(file: UploadFile) -> str:
#     # Save uploaded audio temporarily
#     temp_file = f"temp_{file.filename}"
#     with open(temp_file, "wb") as f:
#         f.write(file.file.read())
    
#     # Transcribe using Whisper
#     result = model.transcribe(temp_file)
#     text = result['text']
    
#     # Clean up
#     import os
#     os.remove(temp_file)
    
#     return text
# Temporary placeholder for STT
def audio_to_text(file):
    # Just return a fixed string for testing
    return "This is a test transcript."
