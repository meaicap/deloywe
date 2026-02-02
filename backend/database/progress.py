from database.db import get_connection
from datetime import datetime

def create_progress_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Quiz results
    cur.execute("""
    CREATE TABLE IF NOT EXISTS quiz_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        topic TEXT,
        score INTEGER,
        total INTEGER,
        created_at TEXT
    )
    """)

    # Flashcard progress
    cur.execute("""
    CREATE TABLE IF NOT EXISTS flashcard_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        question TEXT,
        known INTEGER
    )
    """)

    conn.commit()
    conn.close()


def save_quiz_result(user_id, topic, score, total):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO quiz_results (user_id, topic, score, total, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, topic, score, total,
          datetime.now().strftime("%Y-%m-%d %H:%M")))

    conn.commit()
    conn.close()


def save_flashcard_progress(user_id, question, known):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO flashcard_progress (user_id, question, known)
    VALUES (?, ?, ?)
    """, (user_id, question, known))

    conn.commit()
    conn.close()


def get_quiz_history(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT topic, score, total, created_at
    FROM quiz_results
    WHERE user_id=?
    ORDER BY created_at DESC
    """, (user_id,))

    rows = cur.fetchall()
    conn.close()
    return rows
