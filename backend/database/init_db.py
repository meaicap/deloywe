from database.user import create_user_table
from database.quiz import create_quiz_tables
from database.flashcard import create_flashcard_tables
from database.document import create_document_table



def init_db():
    create_user_table()
    create_quiz_tables()
    create_flashcard_tables()
    create_document_table()
    print("✅ Database initialized successfully")


if __name__ == "__main__":
    init_db()
