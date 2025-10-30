import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("AI_API_KEY"))


def ask_llm_about_profession(profession: str, question: str) -> str:
    prompt = (
        f"Ти — експерт у професії '{profession}'. "
        f"Користувач запитує: {question}\n"
        f"Дай коротку, зрозумілу і точну відповідь українською мовою."
    )

    response = client.models.generate_content(
        model=os.getenv('API_MODEL'),
        contents=prompt
    )

    return response.text
