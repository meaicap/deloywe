from rag.text_splitter import split_text
from rag.vector_store import create_vector_db


def index_document(
    text: str,
    document_id: int
) -> int:
    """
    Chunk → Embed → Lưu ChromaDB
    Gắn document_id cho từng chunk
    """

    # 1️⃣ Chia văn bản thành chunks
    chunks = split_text(text)

    if not chunks:
        raise ValueError("❌ Không có chunk để index")

    # 2️⃣ Lưu vào vector DB (🔥 có document_id)
    create_vector_db(
        text_chunks=chunks,
        document_id=document_id
    )

    print(f"✅ Indexed {len(chunks)} chunks cho document_id={document_id}")
    return len(chunks)
