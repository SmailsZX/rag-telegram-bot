from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings


def get_embeddings() -> OllamaEmbeddings:
    """Эмбеддинги через Ollama (локально)."""
    return OllamaEmbeddings(
        model="nomic-embed-text",
        base_url=settings.ollama_base_url,
    )


def load_documents(data_dir: str) -> list:
    """Загружает все PDF из папки data/."""
    docs = []
    pdf_files = list(Path(data_dir).glob("*.pdf"))

    if not pdf_files:
        print(f"⚠️  В папке {data_dir} нет PDF-файлов.")
        return docs

    for pdf_path in pdf_files:
        print(f"📄 Загружаю: {pdf_path.name}")
        loader = PyPDFLoader(str(pdf_path))
        docs.extend(loader.load())

    print(f"✅ Загружено {len(docs)} страниц из {len(pdf_files)} файлов.")
    return docs


def split_documents(docs: list) -> list:
    """Режет документы на чанки."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"✂️  Получено {len(chunks)} чанков.")
    return chunks


def build_index() -> None:
    """Полный пайплайн: загрузка → чанкинг → эмбеддинги → ChromaDB."""
    print("🚀 Начинаю индексацию...")

    docs = load_documents(settings.data_dir)
    if not docs:
        return

    chunks = split_documents(docs)

    print("🧠 Создаю эмбеддинги и сохраняю в ChromaDB...")
    Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=settings.chroma_dir,
    )
    print(f"✅ Индексация завершена. База: {settings.chroma_dir}")


if __name__ == "__main__":
    build_index()