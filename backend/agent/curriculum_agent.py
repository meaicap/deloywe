from core.llm import client

def extract_topics(text: str):
    prompt = f"""
Bạn là trợ lý học tập.
Hãy phân tích tài liệu sau và liệt kê các chương/chủ đề chính.

Yêu cầu:
- Danh sách dạng gạch đầu dòng
- Mỗi mục ngắn gọn

TÀI LIỆU:
{text[:4000]}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
