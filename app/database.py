import sqlite3
from datetime import datetime
from pathlib import Path


DB_PATH = Path("./chat_history.db")


def init_db() -> None:
    """Создаёт таблицу для логов диалогов, если её нет."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()


def log_message(user_id: int, username: str, question: str, answer: str) -> None:
    """Сохраняет пару вопрос-ответ в БД."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO messages (user_id, username, question, answer, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, username, question, answer, datetime.utcnow().isoformat()),
        )
        conn.commit()


def get_user_stats(user_id: int) -> int:
    """Возвращает количество сообщений пользователя."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT COUNT(*) FROM messages WHERE user_id = ?", (user_id,)
        )
        return cursor.fetchone()[0]