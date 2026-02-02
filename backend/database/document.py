from datetime import datetime
from database.db import get_connection


# =========================
# TẠO BẢNG DOCUMENT
# =========================
def create_document_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        filename TEXT NOT NULL,
        filepath TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


# =========================
# LƯU DOCUMENT
# =========================
def save_document(user_id, filename, filepath):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO documents (user_id, filename, filepath, created_at)
    VALUES (?, ?, ?, ?)
    """, (
        user_id,
        filename,
        filepath,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))

    doc_id = cur.lastrowid
    conn.commit()
    conn.close()
    return doc_id


# =========================
# LẤY DOCUMENT THEO USER
# =========================
def get_documents_by_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, filename, created_at
    FROM documents
    WHERE user_id = ?
    ORDER BY created_at DESC
    """, (user_id,))

    rows = cur.fetchall()
    conn.close()
    return rows


# =========================
# XOÁ DOCUMENT (FIX BUG 2 CLICK)
# =========================
def delete_document(doc_id, user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    DELETE FROM documents
    WHERE id = ? AND user_id = ?
    """, (doc_id, user_id))

    conn.commit()

    deleted = cur.rowcount  # ✅ SỐ ROW ĐÃ XOÁ
    conn.close()

    return deleted > 0
