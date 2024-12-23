import logging
import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Применяем nest_asyncio
nest_asyncio.apply()

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Список вопросов и ответов
questions = {
    "Кто написал 'Отцы и дети'?": "Тургенев",
    "Какой цвет получается при смешивании красного и белого?": "Розовый",
    "Сколько планет в солнечной системе?": "8",
    "Какой элемент имеет химический символ 'O'?": "Кислород",
    "Какой океан самый большой?": "Тихий",
    "Кто написал 'Войну и мир'?": "Толстой",
    "Какой газ составляет большую часть атмосферы Земли?": "Азот",
    "Сколько континентов на Земле?": "7"
}

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я чат-бот с логическими вопросами. Готовы начать?')
    context.user_data['current_question_index'] = 0  # Initialize question index
    await ask_question(update, context)

# Функция для задания вопроса
async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question_index = context.user_data.get('current_question_index', 0)
    if question_index < len(questions):
        question = list(questions.keys())[question_index]
        context.user_data['current_question'] = question
        await update.message.reply_text(question)
    else:
        await update.message.reply_text('Это все вопросы на сегодня!')

# Обработчик текстовых сообщений
async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_answer = update.message.text
    question = context.user_data.get('current_question')

    if question:
        correct_answer = questions[question]
        if user_answer.lower() == correct_answer.lower():
            await update.message.reply_text('Правильно!')
            # Move to the next question
            context.user_data['current_question_index'] += 1
            await ask_question(update, context)
        else:
            await update.message.reply_text(f'Неправильно. Правильный ответ: {correct_answer}')
            # Optionally, you can still ask the next question after a wrong answer
            context.user_data['current_question_index'] += 1
            await ask_question(update, context)

    else:
        await update.message.reply_text('Пожалуйста, ответьте на вопрос, прежде чем запрашивать следующий.')

async def main() -> None:
    # Вставьте сюда свой токен
    application = ApplicationBuilder().token("7696618088:AAGp3HhHuuRcp6BZNRDhTWXY3DQzWl8eDf8").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))

    # Запуск бота
    await application.run_polling()

if __name__ == '__main__':
    # Check if the event loop is already running
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if 'This event loop is already running' in str(e):
            # If the event loop is already running, we can call main() directly
            loop = asyncio.get_event_loop()
            loop.create_task(main())
        else:
            raise