import json
from datetime import datetime
from database.db import get_connection


# =========================
# TẠO BẢNG QUIZ
# =========================
def create_quiz_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Bảng quiz gắn với document
    cur.execute("""
    CREATE TABLE IF NOT EXISTS quiz_templates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        document_id INTEGER,
        title TEXT NOT NULL,
        questions_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (document_id) REFERENCES documents(id)
    )
    """)

    conn.commit()
    conn.close()


# =========================
# LƯU QUIZ MỚI (RETURN ID)
# =========================
def save_quiz(user_id, title, questions, document_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO quiz_templates (
            user_id,
            document_id,
            title,
            questions_json,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            document_id,
            title,
            json.dumps(questions, ensure_ascii=False),
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))

        quiz_id = cur.lastrowid
        conn.commit()
        conn.close()

        return quiz_id

    except Exception as e:
        print("❌ DB SAVE QUIZ ERROR:", e)
        return None


# =========================
# LẤY DANH SÁCH QUIZ (THEO FILE)
# =========================
def get_all_quizzes(user_id, document_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, title, created_at
    FROM quiz_templates
    WHERE user_id = ? AND document_id = ?
    ORDER BY created_at DESC
    """, (user_id, document_id))

    rows = cur.fetchall()
    conn.close()
    return rows


# =========================
# LẤY QUIZ THEO ID
# =========================
def get_quiz_by_id(quiz_id, user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT questions_json
    FROM quiz_templates
    WHERE id = ? AND user_id = ?
    """, (quiz_id, user_id))

    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return json.loads(row[0])


# =========================
# XOÁ QUIZ
# =========================
def delete_quiz(quiz_id, user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    DELETE FROM quiz_templates
    WHERE id = ? AND user_id = ?
    """, (quiz_id, user_id))

    conn.commit()
    conn.close()
