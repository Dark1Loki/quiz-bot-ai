# handlers/quiz.py

from aiogram import types, Dispatcher, F
from aiogram.filters.command import Command

from services.quiz_logic import get_question
from services.db import get_state, update_state
from data.questions import quiz_data

# Старт квиза — сбрасывает прогресс
async def cmd_quiz(message: types.Message):
    await message.answer("Начнем квиз!")
    await update_state(message.from_user.id, question_index=0, correct_answers=0)
    await get_question(message, message.from_user.id)

# Универсальный обработчик ответа
async def handle_answer(callback: types.CallbackQuery):
    selected_index = int(callback.data)
    current_index, correct_answers = await get_state(callback.from_user.id)
    question = quiz_data[current_index]
    correct_index = question['correct_option']

    user_answer = question['options'][selected_index]
    correct_text = question['options'][correct_index]
    is_correct = selected_index == correct_index

    # Удаляем inline-клавиатуру
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Показываем результат
    if is_correct:
        correct_answers += 1
        await callback.message.answer(f"Вы выбрали: {user_answer}. Верно!")
    else:
        await callback.message.answer(
            f"Вы выбрали: {user_answer}. Неверно.\nПравильный ответ: {correct_text}"
        )

    current_index += 1
    await update_state(callback.from_user.id, question_index=current_index, correct_answers=correct_answers)

    if current_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        total = len(quiz_data)
        percent = round((correct_answers / total) * 100)
        await callback.message.answer(
            f"Квиз завершён!\nВаш результат: {correct_answers}/{total} правильных ответов ({percent}%)"
        )

# Регистрация хэндлеров
def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_quiz, Command("quiz"))
    dp.message.register(cmd_quiz, F.text == "Начать игру")
    dp.callback_query.register(handle_answer)