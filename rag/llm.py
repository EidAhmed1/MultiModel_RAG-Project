import os

import google.generativeai as genai
from dotenv import load_dotenv

from rag.prompt import SYSTEM_PROMPT


load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_answer(question, context):

    prompt = SYSTEM_PROMPT.format(
        question=question,
        context=context
    )


    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.1,
            "max_output_tokens": 500
        }
    )


    if response.text:
        return response.text


    return "No answer generated."