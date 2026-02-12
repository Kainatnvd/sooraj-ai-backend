from gtts import gTTS

def text_to_speech(text: str, lang: str = "en") -> str:
    audio_path = "temp_reply.mp3"  # keep same path so frontend can play
    tts = gTTS(text=text, lang=lang)
    tts.save(audio_path)
    return audio_path
