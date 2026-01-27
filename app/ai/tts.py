# from gtts import gTTS
# import os

# def text_to_speech(text: str, lang: str = "en") -> str:
#     audio_filename = f"audio_{hash(text)}.mp3"
#     tts = gTTS(text=text, lang=lang)
#     tts.save(f"app/vectorstore/{audio_filename}")
#     return audio_filename
# Temporary placeholder for TTS
def text_to_speech(text, lang="en"):
    # Just return a dummy file path
    return "dummy_audio.mp3"
