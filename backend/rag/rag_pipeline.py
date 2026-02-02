# from rag.vector_store import load_vector_db
# from core.llm import client

# def rag_answer(question: str):
#     vectordb = load_vector_db()

#     docs = vectordb.similarity_search(question, k=4)

#     context = "\n\n".join([doc.page_content for doc in docs])

#     prompt = f"""
# Bạn là trợ lý học tập.
# Chỉ sử dụng thông tin trong tài liệu dưới đây để trả lời.
# Nếu không tìm thấy thông tin, hãy nói "Không tìm thấy trong tài liệu".

# TÀI LIỆU:
# {context}

# CÂU HỎI:
# {question}
# """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}]
#     )

#     return response.choices[0].message.content
