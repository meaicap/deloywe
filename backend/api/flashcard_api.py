from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from agent.flashcard_agent import generate_flashcards_from_context
from database.flashcard import (
    save_flashcard_set,
    get_all_flashcard_sets,
    get_flashcard_set_by_id,
    delete_flashcard_set
)

router = APIRouter(prefix="/flashcard", tags=["Flashcard"])


# =====================
# SCHEMA
# =====================
class FlashcardCreateRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    document_id: int = Field(..., gt=0)
    title: Optional[str] = None          # ✅ KHÔNG BẮT BUỘC
    num_cards: int = Field(default=10, ge=1, le=20)


class FlashcardResponse(BaseModel):
    question: str
    answer: str


class FlashcardCreateResponse(BaseModel):
    message: str
    set_id: int
    total_cards: int
    cards: List[FlashcardResponse]


# =====================
# CREATE FLASHCARD (RAG – THEO FILE)
# =====================
@router.post("/create", response_model=FlashcardCreateResponse)
def create_flashcard(data: FlashcardCreateRequest):

    # ===== AUTO TITLE NẾU KHÔNG CÓ =====
    title = data.title
    if not title:
        title = f"Flashcard - Document {data.document_id} - {datetime.now().strftime('%d/%m/%Y %H:%M')}"

    # ===== GENERATE FLASHCARDS =====
    cards = generate_flashcards_from_context(
        document_id=data.document_id,
        num_cards=data.num_cards
    )

    if not cards:
        raise HTTPException(
            status_code=500,
            detail="❌ Không tạo được flashcard từ tài liệu"
        )

    # ===== SAVE FLASHCARD SET =====
    set_id = save_flashcard_set(
        user_id=data.user_id,
        document_id=data.document_id,
        title=title,
        cards=cards
    )

    if not set_id:
        raise HTTPException(
            status_code=500,
            detail="❌ Lỗi lưu flashcard vào database"
        )

    return {
        "message": "✅ Flashcard created successfully",
        "set_id": set_id,
        "total_cards": len(cards),
        "cards": cards
    }


# =====================
# LIST FLASHCARD SETS (THEO DOCUMENT)
# =====================
@router.get("/list/{user_id}")
def list_flashcards(
    user_id: int,
    document_id: int = Query(..., gt=0)
):
    """
    Lấy danh sách flashcard theo FILE (document)
    """
    return get_all_flashcard_sets(user_id, document_id)


# =====================
# GET FLASHCARD SET DETAIL
# =====================
@router.get("/{set_id}")
def get_flashcard(set_id: int, user_id: int):
    cards = get_flashcard_set_by_id(set_id, user_id)
    if not cards:
        raise HTTPException(
            status_code=404,
            detail="❌ Flashcard set not found"
        )

    return {
        "set_id": set_id,
        "total_cards": len(cards),
        "cards": cards
    }


# =====================
# DELETE FLASHCARD SET
# =====================
@router.delete("/{set_id}")
def remove_flashcard(set_id: int, user_id: int):
    delete_flashcard_set(set_id, user_id)
    return {"message": "🗑️ Flashcard deleted"}
