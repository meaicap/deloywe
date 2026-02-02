from core.llm import client

def generate_study_plan(topics: list):
    topic_text = "\n".join(topics)

    prompt = f"""
Dựa trên các chủ đề sau, hãy đề xuất lộ trình ôn tập cho sinh viên.

Yêu cầu:
- Chia theo tuần
- Từ dễ đến khó
- Có gợi ý học tập

CHỦ ĐỀ:
{topic_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
