# backend/core/llm.py

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load biến môi trường từ file .env (ở gốc project)
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY chưa được thiết lập trong file .env")

# Khởi tạo OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def chat_with_ai(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Bạn là trợ lý học tập thông minh."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()
