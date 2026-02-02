import sqlite3
import os

DB_NAME = "data/database.db"
os.makedirs("data", exist_ok=True)

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
