
# rag/llms.py
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def ask_gemini(prompt: str):
    """Free Gemini model via OpenRouter"""
    response = client.chat.completions.create(
        model="google/gemini-3-flash-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content


def ask_deepseek(prompt: str):
    """Free DeepSeek R1 variant"""
    response = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528:free",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content
