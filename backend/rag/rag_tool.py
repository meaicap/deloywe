from rag.vector_store import load_vector_db
from core.llm import client

# =====================
# CONFIG
# =====================
MAX_CONTEXT_CHARS = 4000
MIN_CONTEXT_CHARS = 200
MIN_CHUNK_LENGTH = 40


# ======================================================
# CORE: RETRIEVE CONTEXT BY DOCUMENT_ID (🔥 QUAN TRỌNG)
# ======================================================
def retrieve_context_by_document(
    document_id: int,
    query: str,
    k: int = 6
) -> str:
    """
    Lấy ngữ cảnh học tập từ VectorDB (RAG)
    → CHỈ LẤY CHUNK CỦA document_id ĐƯỢC CHỌN
    """

    try:
        vectordb = load_vector_db()

        docs = vectordb.similarity_search(
            query,
            k=k,
            filter={
                "document_id": document_id
            }
        )

    except Exception as e:
        print("❌ RAG search error:", e)
        return ""

    if not docs:
        print(f"⚠️ RAG: Không tìm thấy chunk cho document_id={document_id}")
        return ""

    contexts = []
    total_chars = 0

    for doc in docs:
        content = doc.page_content.strip()

        if not content:
            continue

        if len(content) < MIN_CHUNK_LENGTH:
            continue

        contexts.append(content)
        total_chars += len(content)

        if total_chars >= MAX_CONTEXT_CHARS:
            break

    final_context = "\n\n".join(contexts)

    # DEBUG
    print("====== RAG CONTEXT PREVIEW ======")
    print(final_context[:800])
    print("====== END CONTEXT ======")

    if len(final_context) < MIN_CONTEXT_CHARS:
        print("⚠️ Context quá ngắn:", len(final_context))
        return ""

    return final_context


# ======================================================
# BACKWARD COMPAT (NẾU SAU NÀY CẦN RAG GLOBAL)
# ======================================================
def retrieve_context(query: str, k: int = 6) -> str:
    """
    RAG không gắn document_id (dự phòng)
    """
    try:
        vectordb = load_vector_db()
        docs = vectordb.similarity_search(query, k=k)
    except Exception as e:
        print("❌ RAG search error:", e)
        return ""

    contexts = []
    total_chars = 0

    for doc in docs:
        content = doc.page_content.strip()
        if not content or len(content) < MIN_CHUNK_LENGTH:
            continue

        contexts.append(content)
        total_chars += len(content)
        if total_chars >= MAX_CONTEXT_CHARS:
            break

    final_context = "\n\n".join(contexts)
    if len(final_context) < MIN_CONTEXT_CHARS:
        return ""

    return final_context


# ======================================================
# RAG ANSWER (DÙNG CHO CHATBOX)
# ======================================================
def rag_answer(
    question: str,
    document_id: int
) -> str:
    """
    Trả lời dựa trên RAG
    → GẮN CHẶT THEO document_id
    """

    retrieve_query = f"""
    Khái niệm, định nghĩa, nguyên lý, công thức,
    nội dung học tập quan trọng liên quan đến:
    {question}
    """

    context = retrieve_context_by_document(
        document_id=document_id,
        query=retrieve_query
    )

    if not context:
        return "Không tìm thấy thông tin trong tài liệu."

    prompt = f"""
Bạn là trợ lý học tập.

NHIỆM VỤ:
- Chỉ sử dụng thông tin trong tài liệu
- Trả lời NGẮN GỌN, RÕ RÀNG
- Dạng học tập (định nghĩa, giải thích, gạch đầu dòng)
- KHÔNG dùng câu chung chung
- KHÔNG tự suy đoán

TÀI LIỆU:
\"\"\" 
{context}
\"\"\" 

CÂU HỎI:
{question}

TRẢ LỜI:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    return response.choices[0].message.content.strip()
