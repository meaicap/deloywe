from core.llm import client
from rag.rag_tool import retrieve_context_by_document
import json
from typing import List, Dict

# =====================
# CONFIG
# =====================
MAX_CARDS = 10


def generate_flashcards_from_context(
    document_id: int,
    num_cards: int = MAX_CARDS
) -> List[Dict[str, str]]:
    """
    Generate flashcards CHUẨN RAG – THEO FILE
    """

    # =====================
    # 1️⃣ GET CONTEXT (THEO document_id)
    # =====================
    context = retrieve_context_by_document(
        document_id=document_id,
        query="""
        Trích xuất các khái niệm học tập QUAN TRỌNG:
        - Định nghĩa
        - Nguyên lý
        - Ý chính dễ ra đề
        """,
        k=8
    )

    if not context:
        return _fallback_cards(num_cards)

    # =====================
    # 2️⃣ PROMPT TẠO FLASHCARD
    # =====================
    prompt = f"""
Bạn là AI hỗ trợ ôn thi.

CHỈ sử dụng thông tin trong tài liệu.
KHÔNG suy đoán.
KHÔNG viết chung chung.

NHIỆM VỤ:
- Tạo {num_cards} flashcard học tập CHUẨN
- Mỗi flashcard tập trung 1 ý
- Ưu tiên định nghĩa, nguyên lý, kiến thức dễ ra đề

YÊU CẦU:
- Câu hỏi rõ ràng
- Trả lời ngắn gọn, súc tích
- Dạng ghi nhớ nhanh

FORMAT JSON THUẦN:
[
  {{
    "question": "Câu hỏi ôn tập",
    "answer": "Câu trả lời ngắn gọn"
  }}
]

TÀI LIỆU:
\"\"\"
{context}
\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.15
        )

        raw = response.choices[0].message.content.strip()

        if raw.startswith("```"):
            raw = raw.replace("```json", "").replace("```", "").strip()

        cards = json.loads(raw)

        if isinstance(cards, list):
            valid_cards = [
                c for c in cards
                if "question" in c and "answer" in c
            ]
            return valid_cards[:num_cards]

    except Exception as e:
        print("❌ Flashcard error:", e)

    return _fallback_cards(num_cards)


# =====================
# FALLBACK (CHỈ DÙNG KHI RAG FAIL)
# =====================
def _fallback_cards(n: int) -> List[Dict[str, str]]:
    return [
        {
            "question": f"Khái niệm {i + 1}",
            "answer": "Không trích xuất được từ tài liệu"
        }
        for i in range(n)
    ]
