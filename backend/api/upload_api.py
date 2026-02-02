from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pathlib import Path
import pdfplumber
import shutil
import uuid

from rag.indexer import index_document
from database.document import save_document

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

# ===================== CONFIG =====================
UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ===================== UPLOAD PDF =====================
@router.post("/pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    user_id: int = Form(...)
):
    """
    Upload PDF
    → save file
    → save DB (documents)
    → extract text
    → index RAG (THEO document_id)
    """

    # 1️⃣ Validate file
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="❌ Chỉ hỗ trợ file PDF")

    try:
        # 2️⃣ Tạo tên file không trùng
        file_id = str(uuid.uuid4())
        filename = f"{file_id}_{file.filename}"
        file_path = UPLOAD_DIR / filename

        # 3️⃣ Lưu file vào disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 4️⃣ Trích xuất text từ PDF
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

        if not text.strip():
            raise HTTPException(status_code=400, detail="❌ PDF không có nội dung")

        # 5️⃣ Lưu document vào database
        document_id = save_document(
            user_id=user_id,
            filename=file.filename,
            filepath=str(file_path)
        )

        # 6️⃣ Index RAG (🔥 TRUYỀN document_id)
        total_chunks = index_document(
            text=text,
            document_id=document_id
        )

        return {
            "message": "✅ Upload & lưu tài liệu thành công",
            "document_id": document_id,
            "filename": file.filename,
            "total_chunks": total_chunks
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
