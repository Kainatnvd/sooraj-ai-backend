# # app/ai/chatbot.py
# import os
# from dotenv import load_dotenv
# # Load .env file
# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
# try:
#     import openai
#     openai.api_key = os.getenv("OPENAI_API_KEY")
#     print("OpenAI API Key Loaded:", bool(openai.api_key))
#     OPENAI_AVAILABLE = True
# except ImportError:
#     OPENAI_AVAILABLE = False

# def get_reply(message: str, language: str = "ur") -> str:
#     """
#     Get AI response from ChatGPT-4-mini.
#     If API is not available, return a mock response.
#     """
#     # Mock fallback
#     if not OPENAI_AVAILABLE or not os.getenv("OPENAI_API_KEY"):
#         if language == "ur":
#             return "یہ ایک ٹیسٹ جواب ہے، API ابھی دستیاب نہیں۔"
#         elif language == "pa":
#             return "ایہ اک ٹیسٹ جواب ہے، API ہن تک دستیاب نہیں۔"
#         else:
#             return "This is a test reply, API not available yet."

#     # Real API call
#     system_prompt = "You are a helpful assistant for farmers. Answer questions about crops, diseases, and fertilizers in the requested language."
#     language_prompt = {
#     "ur": "Answer in Urdu.",
#     "pa": "Answer in Punjabi (Shahmukhi script).",
#     "en": "Answer in English."
# }


#     try:
#         response = openai.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": f"{message}\n{language_prompt.get(language, 'Answer in Urdu.')}"}
#             ],
#             temperature=0.7,
#             max_tokens=500
#         )
#         reply = response.choices[0].message.content.strip()
#         return reply
#     except Exception as e:
#         print(f"Error calling OpenAI API: {e}")
#         return "معاف کریں، فی الحال میں جواب نہیں دے سکتا۔"
# app/ai/chatbot.py
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

try:
    import openai
    openai.api_key = os.getenv("API_KEY")
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

def get_reply(message: str, language: str = "ur") -> str:
    """
    Get AI response from ChatGPT-4-mini.
    Will respond in Urdu, Punjabi (Shahmukhi), or English based on detected language.
    """
    if not OPENAI_AVAILABLE or not os.getenv("OPENAI_API_KEY"):
        # fallback
        return {
            "ur": "یہ ایک ٹیسٹ جواب ہے، API دستیاب نہیں۔",
            "pa": "ایہ اک ٹیسٹ جواب ہے، API ہن تک دستیاب نہیں۔",
            "en": "This is a test reply, API not available."
        }.get(language, "This is a test reply.")

    # Prompts for GPT
    system_prompt = (
        "You are a helpful assistant for farmers. "
        "Answer questions about crops, diseases, and fertilizers "
        "in the language requested by the user."
    )

    language_prompt = {
        "ur": "Answer in Urdu.",
        "pa": "Answer in Punjabi (Shahmukhi script).",
        "en": "Answer in English."
    }

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{message}\n{language_prompt.get(language, 'Answer in English.')}"}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"OpenAI API error: {e}")
        return {
            "ur": "معاف کریں، فی الحال میں جواب نہیں دے سکتا۔",
            "pa": "معاف کریں، فی الحال میں جواب نہیں دے سکتا۔",
            "en": "Sorry, I cannot respond right now."
        }.get(language, "Sorry, I cannot respond right now.")
