from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.config import settings
from app.indexer import get_embeddings
from app.prompts import SYSTEM_PROMPT, USER_PROMPT


def get_llm() -> ChatOllama:
    """Локальная LLM через Ollama."""
    return ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=0.1,
    )


def get_vectorstore() -> Chroma:
    """Подключается к существующей ChromaDB."""
    return Chroma(
        persist_directory=settings.chroma_dir,
        embedding_function=get_embeddings(),
    )


def format_docs(docs: list) -> str:
    """Склеивает найденные чанки в один контекст."""
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def ask(question: str) -> str:
    """Главная функция: retrieval + генерация."""
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": settings.top_k}
    )

    docs = retriever.invoke(question)
    context = format_docs(docs)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", USER_PROMPT),
    ])

    chain = prompt | get_llm() | StrOutputParser()

    answer = chain.invoke({
        "context": context,
        "question": question,
    })

    return answer