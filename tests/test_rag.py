"""Тесты RAG-пайплайна (без вызова LLM)."""

from app.rag import format_docs
from app.prompts import SYSTEM_PROMPT, USER_PROMPT


def test_format_docs_empty():
    """Пустой список → пустая строка."""
    assert format_docs([]) == ""


def test_format_docs_single():
    """Один документ → его текст."""
    class Doc:
        page_content = "Текст документа"

    assert format_docs([Doc()]) == "Текст документа"


def test_format_docs_multiple():
    """Несколько документов → склеены через разделитель."""
    class Doc:
        def __init__(self, text):
            self.page_content = text

    docs = [Doc("Первый"), Doc("Второй")]
    result = format_docs(docs)
    assert "Первый" in result
    assert "Второй" in result
    assert "---" in result


def test_system_prompt_has_context_placeholder():
    """В системном промпте есть {context}."""
    assert "{context}" in SYSTEM_PROMPT


def test_user_prompt_has_question_placeholder():
    """В пользовательском промпте есть {question}."""
    assert "{question}" in USER_PROMPT


def test_system_prompt_has_no_hallucination_rule():
    """В промпте есть правило про отсутствие информации."""
    assert "нет ответа" in SYSTEM_PROMPT.lower() or "нет информации" in SYSTEM_PROMPT.lower()