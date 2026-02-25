# # from gtts import gTTS

# # def text_to_speech(text: str, lang: str = "en") -> str:
# #     audio_path = "temp_reply.mp3"  # keep same path so frontend can play
# #     tts = gTTS(text=text, lang=lang)
# #     tts.save(audio_path)
# #     return audio_path
# from gtts import gTTS
# import tempfile

# def text_to_speech(text: str, lang: str = "en") -> str:
#     tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
#     tmp_path = tmp.name
#     tmp.close()

#     tts = gTTS(text=text, lang=lang)
#     tts.save(tmp_path)

#     return tmp_path
# import tempfile
# from gtts import gTTS

# def text_to_speech(text: str, lang: str = "en") -> str:
#     tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
#     tts = gTTS(text=text, lang=lang)
#     tts.save(tmp.name)
#     return tmp.name
import tempfile
from gtts import gTTS
import os

def text_to_speech(text: str, lang: str = "en") -> str:
    """
    Converts text to speech and saves it as a temporary .mp3 file.
    
    Args:
        text (str): The text to convert to speech.
        lang (str): Language code for gTTS ('en', 'ur', 'pa', etc.).
    
    Returns:
        str: Path to the generated temporary audio file (.mp3)
    """
    # Ensure text is not empty
    if not text.strip():
        raise ValueError("Cannot generate speech from empty text.")
    
    # Create a temporary file
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp_path = tmp_file.name
    tmp_file.close()  # Close so gTTS can write to it

    # Generate speech
    tts = gTTS(text=text, lang=lang)
    tts.save(tmp_path)

    return tmp_path