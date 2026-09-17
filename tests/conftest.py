"""Фикстуры для тестов."""

import pytest
from pathlib import Path


@pytest.fixture
def temp_db(tmp_path):
    """Временная БД для тестов логирования."""
    db_path = tmp_path / "test_chat_history.db"
    return db_path


@pytest.fixture
def sample_docs():
    """Примеры документов для тестов RAG."""
    return [
        "Python — это высокоуровневый язык программирования.",
        "FastAPI — современный веб-фреймворк для Python.",
        "PostgreSQL — объектно-реляционная СУБД.",
    ]


@pytest.fixture
def test_data_dir(tmp_path):
    """Временная папка для PDF."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir