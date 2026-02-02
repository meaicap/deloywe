import sqlite3
from datetime import datetime
from database.db import get_connection


# =========================
# CREATE TABLES
# =========================
def create_flashcard_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flashcard_sets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        document_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (document_id) REFERENCES documents(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flashcards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        set_id INTEGER NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        FOREIGN KEY (set_id) REFERENCES flashcard_sets(id)
            ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()


# =========================
# SAVE FLASHCARD SET
# =========================
def save_flashcard_set(
    user_id: int,
    document_id: int,
    title: str,
    cards: list
) -> int | None:

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO flashcard_sets (
            user_id,
            document_id,
            title,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """, (
            user_id,
            document_id,
            title,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))

        set_id = cursor.lastrowid

        for card in cards:
            cursor.execute("""
            INSERT INTO flashcards (set_id, question, answer)
            VALUES (?, ?, ?)
            """, (
                set_id,
                card["question"],
                card["answer"]
            ))

        conn.commit()
        return set_id

    except Exception as e:
        conn.rollback()
        print("❌ DB ERROR save_flashcard_set:", e)
        return None

    finally:
        conn.close()


# =========================
# LIST FLASHCARD SETS (THEO DOCUMENT)
# =========================
def get_all_flashcard_sets(user_id: int, document_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, title, created_at
    FROM flashcard_sets
    WHERE user_id = ? AND document_id = ?
    ORDER BY created_at DESC
    """, (user_id, document_id))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "title": r[1],
            "created_at": r[2]
        }
        for r in rows
    ]


# =========================
# GET FLASHCARD SET DETAIL
# =========================
def get_flashcard_set_by_id(set_id: int, user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT fc.question, fc.answer
    FROM flashcards fc
    JOIN flashcard_sets fs ON fc.set_id = fs.id
    WHERE fs.id = ? AND fs.user_id = ?
    """, (set_id, user_id))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "question": r[0],
            "answer": r[1]
        }
        for r in rows
    ]


# =========================
# DELETE FLASHCARD SET
# =========================
def delete_flashcard_set(set_id: int, user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM flashcard_sets
    WHERE id = ? AND user_id = ?
    """, (set_id, user_id))

    conn.commit()
    conn.close()
