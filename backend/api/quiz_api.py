from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

from agent.question_agent import generate_mcq_from_context
from database.quiz import (
    save_quiz,
    get_all_quizzes,
    get_quiz_by_id,
    delete_quiz
)

router = APIRouter(prefix="/quiz", tags=["Quiz"])


# ======================
# SCHEMAS
# ======================
class QuizCreateRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    document_id: int = Field(..., gt=0)
    title: Optional[str] = None          # ✅ KHÔNG BẮT BUỘC
    num_questions: Optional[int] = 10


class QuizQuestionResponse(BaseModel):
    question: str
    options: Dict[str, str]
    correct_answer: str


class QuizCreateResponse(BaseModel):
    message: str
    quiz_id: int
    total_questions: int
    quiz: List[QuizQuestionResponse]


# ======================
# CREATE QUIZ (RAG – THEO FILE)
# ======================
@router.post("/create", response_model=QuizCreateResponse)
def create_quiz(data: QuizCreateRequest):

    # ===== VALIDATE SỐ CÂU =====
    num_questions = data.num_questions or 10
    if num_questions <= 0:
        raise HTTPException(
            status_code=400,
            detail="❌ num_questions phải > 0"
        )

    # ===== TỰ SINH TITLE NẾU KHÔNG CÓ =====
    title = data.title
    if not title:
        title = f"Quiz - Document {data.document_id} - {datetime.now().strftime('%d/%m/%Y %H:%M')}"

    # ===== SINH CÂU HỎI =====
    questions = generate_mcq_from_context(
        document_id=data.document_id,
        num_questions=num_questions
    )

    if not questions:
        raise HTTPException(
            status_code=500,
            detail="❌ Không tạo được câu hỏi trắc nghiệm"
        )

    # ===== LƯU QUIZ =====
    quiz_id = save_quiz(
        user_id=data.user_id,
        title=title,
        questions=questions,
        document_id=data.document_id
    )

    if not quiz_id:
        raise HTTPException(
            status_code=500,
            detail="❌ Lỗi lưu quiz vào database"
        )

    return {
        "message": "✅ Quiz created successfully",
        "quiz_id": quiz_id,
        "total_questions": len(questions),
        "quiz": questions
    }


# ======================
# LIST QUIZ (THEO FILE)
# ======================
@router.get("/list/{user_id}")
def list_quiz(
    user_id: int,
    document_id: int = Query(..., gt=0)
):
    return get_all_quizzes(user_id, document_id)


# ======================
# GET QUIZ DETAIL
# ======================
@router.get("/{quiz_id}")
def get_quiz(
    quiz_id: int,
    user_id: int
):
    quiz = get_quiz_by_id(quiz_id, user_id)
    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="❌ Quiz not found"
        )
    return quiz


# ======================
# DELETE QUIZ
# ======================
@router.delete("/{quiz_id}")
def remove_quiz(
    quiz_id: int,
    user_id: int
):
    delete_quiz(quiz_id, user_id)
    return {"message": "🗑️ Quiz deleted"}
