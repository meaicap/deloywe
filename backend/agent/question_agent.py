from core.llm import client
from rag.rag_tool import retrieve_context_by_document
import json
import random
from typing import List, Dict


def generate_mcq_from_context(
    document_id: int,
    document_text: str | None = None,
    num_questions: int = 10
) -> List[Dict]:
    """
    Sinh câu hỏi trắc nghiệm ôn tập bằng RAG
    → GẮN CHẶT THEO document_id
    """

    # =====================
    # 1️⃣ GET CONTEXT (RAG)
    # =====================
    if document_text and document_text.strip():
        context = document_text
    else:
        context = retrieve_context_by_document(
            document_id=document_id,
            query="""
            Khái niệm cốt lõi, định nghĩa, nguyên lý,
            kiến thức trọng tâm dùng để ôn thi
            """,
            k=10
        )

    if not context:
        return _fallback_quiz(num_questions)

    context = context[:6000]

    # =====================
    # 2️⃣ PROMPT
    # =====================
    prompt = f"""
Bạn là AI hỗ trợ ôn tập cho sinh viên.

CHỈ sử dụng thông tin trong tài liệu bên dưới.
KHÔNG bịa kiến thức.
Nếu thông tin chưa đủ, tạo câu hỏi mức khái niệm chung.

NHIỆM VỤ:
- Sinh {num_questions} câu hỏi trắc nghiệm ôn tập
- Không chia chương, mục

YÊU CẦU:
- Tập trung định nghĩa, nguyên lý
- Phù hợp ôn thi

CHỈ TRẢ VỀ JSON THUẦN:
[
  {{
    "question": "...",
    "options": {{
      "A": "...",
      "B": "...",
      "C": "...",
      "D": "..."
    }},
    "correct_answer": "A"
  }}
]

TÀI LIỆU:
\"\"\"
{context}
\"\"\"
"""

    # =====================
    # 3️⃣ CALL LLM
    # =====================
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        raw = response.choices[0].message.content.strip()

        if raw.startswith("```"):
            raw = raw.replace("```json", "").replace("```", "").strip()

        quiz = json.loads(raw)

        if not isinstance(quiz, list):
            raise ValueError("Output is not list")

        return quiz[:num_questions]

    except Exception as e:
        print("❌ QUIZ GENERATION ERROR:", e)
        return _fallback_quiz(num_questions)


# =====================
# FALLBACK (CHỈ DÙNG KHI RAG FAIL)
# =====================
def _fallback_quiz(n: int) -> List[Dict]:
    options_keys = ["A", "B", "C", "D"]
    quiz = []

    for i in range(n):
        correct = random.choice(options_keys)
        quiz.append({
            "question": f"Khái niệm quan trọng #{i+1} trong tài liệu là gì?",
            "options": {
                "A": "Đáp án A",
                "B": "Đáp án B",
                "C": "Đáp án C",
                "D": "Đáp án D"
            },
            "correct_answer": correct
        })

    return quiz
