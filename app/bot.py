import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from app.config import settings
from app.database import get_user_stats, init_db, log_message
from app.rag import ask

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

bot = Bot(token=settings.bot_token)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer(
        "👋 Привет! Я RAG-бот.\n\n"
        "Задай мне вопрос — я поищу ответ в базе знаний.\n\n"
        "Команды:\n"
        "/start — это сообщение\n"
        "/stats — сколько вопросов ты задал\n"
        "/help — помощь"
    )


@dp.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "Просто напиши вопрос — я найду ответ в загруженных документах.\n"
        "Если ответа нет — честно скажу об этом."
    )


@dp.message(Command("stats"))
async def cmd_stats(message: Message) -> None:
    count = get_user_stats(message.from_user.id)
    await message.answer(f"📊 Ты задал {count} вопрос(ов).")


@dp.message(F.text)
async def handle_question(message: Message) -> None:
    question = message.text.strip()

    if not question:
        return

    logger.info(f"Вопрос от {message.from_user.id}: {question}")

    # Показываем «печатает...»
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    try:
        answer = ask(question)
    except Exception as e:
        logger.exception("Ошибка при обработке вопроса")
        await message.answer(
            "⚠️ Произошла ошибка при обработке вопроса. Попробуй позже."
        )
        return

    # Логируем в БД
    username = message.from_user.username or message.from_user.full_name
    log_message(message.from_user.id, username, question, answer)

    # Telegram ограничивает длину сообщения 4096 символами
    for i in range(0, len(answer), 4000):
        await message.answer(answer[i:i + 4000])


async def start_bot() -> None:
    """Точка входа для запуска бота."""
    init_db()
    logger.info("Бот запущен.")
    await dp.start_polling(bot)