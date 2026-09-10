"""Скрипт для индексации PDF-документов из папки data/.

Запуск:
    python -m scripts.index_documents
"""

from app.indexer import build_index


if __name__ == "__main__":
    build_index()