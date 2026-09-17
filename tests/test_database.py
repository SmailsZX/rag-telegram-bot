"""Тесты SQLite-логирования."""

import sqlite3

from app import database


def test_init_db(tmp_path, monkeypatch):
    """Создаётся таблица messages."""
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(database, "DB_PATH", db_path)

    database.init_db()

    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='messages'"
        )
        assert cursor.fetchone() is not None


def test_log_message(tmp_path, monkeypatch):
    """Сообщение записывается в БД."""
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(database, "DB_PATH", db_path)

    database.init_db()
    database.log_message(123, "test_user", "Вопрос", "Ответ")

    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("SELECT user_id, question, answer FROM messages")
        row = cursor.fetchone()
        assert row == (123, "Вопрос", "Ответ")


def test_get_user_stats(tmp_path, monkeypatch):
    """Счётчик сообщений работает."""
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(database, "DB_PATH", db_path)

    database.init_db()
    database.log_message(123, "test_user", "В1", "О1")
    database.log_message(123, "test_user", "В2", "О2")

    assert database.get_user_stats(123) == 2


def test_get_user_stats_empty(tmp_path, monkeypatch):
    """Счётчик для нового пользователя = 0."""
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(database, "DB_PATH", db_path)

    database.init_db()
    assert database.get_user_stats(999) == 0