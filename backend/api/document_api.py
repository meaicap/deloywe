from fastapi import APIRouter, HTTPException
from database.document import (
    get_documents_by_user,
    delete_document
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


# =========================
# GET DOCUMENTS BY USER
# =========================
@router.get("/user/{user_id}")
def list_user_documents(user_id: int):
    """
    Lấy danh sách file PDF của user
    """
    docs = get_documents_by_user(user_id)

    return [
        {
            "id": d[0],
            "filename": d[1],
            "created_at": d[2]
        }
        for d in docs
    ]


# =========================
# DELETE DOCUMENT
# =========================
@router.delete("/{document_id}")
def remove_document(document_id: int, user_id: int):
    """
    Xóa document theo id (chỉ owner mới xóa được)
    """
    success = delete_document(document_id, user_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="❌ Document không tồn tại hoặc không có quyền xóa"
        )

    return {"message": "🗑️ Document deleted successfully"}
