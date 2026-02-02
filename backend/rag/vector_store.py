from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import os
from typing import List

CHROMA_DB_PATH = "data/chroma_db"
COLLECTION_NAME = "documents"


def get_embeddings():
    return OpenAIEmbeddings()


def get_or_create_vector_db():
    """
    Load hoặc tạo mới ChromaDB (KHÔNG ghi đè dữ liệu cũ)
    """
    os.makedirs(CHROMA_DB_PATH, exist_ok=True)

    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DB_PATH,
        embedding_function=get_embeddings()
    )


def create_vector_db(
    text_chunks: List[str],
    document_id: int
):
    """
    Thêm chunks vào ChromaDB
    Gắn metadata document_id cho từng chunk
    """

    vectordb = get_or_create_vector_db()

    metadatas = [
        {"document_id": document_id}
        for _ in text_chunks
    ]

    vectordb.add_texts(
        texts=text_chunks,
        metadatas=metadatas
    )

    return vectordb


def load_vector_db():
    """
    Load ChromaDB để search
    """
    if not os.path.exists(CHROMA_DB_PATH):
        raise RuntimeError("❌ ChromaDB chưa tồn tại – hãy upload PDF hoặc index trước")

    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DB_PATH,
        embedding_function=get_embeddings()
    )
