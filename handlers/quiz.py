# handlers/quiz.py

from aiogram import types, Dispatcher, F
from aiogram.filters.command import Command

from services.quiz_logic import ask
from services.db import get_state, update_state
from data.questions import quiz_data

# запуск квиза
async def cmd_quiz(message: types.Message):
    await message.answer("Начнем квиз!")
    await update_state(message.from_user.id, q_idx=0, ok_count=0)
    await ask(message, message.from_user.id)

async def handle_answer(callback: types.CallbackQuery):
    picked = int(callback.data)
    step, ok_count = await get_state(callback.from_user.id)
    question = quiz_data[step]
    right = question['correct_option']

    user_answer = question['options'][picked]
    correct_text = question['options'][right]
    is_correct = picked == right

    # Удаляем inline-клавиатуру
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Показываем результат
    if is_correct:
        ok_count += 1
        await callback.message.answer(f"Вы выбрали: {user_answer}. Верно!")
    else:
        await callback.message.answer(
            f"Вы выбрали: {user_answer}. Неверно.\nПравильный ответ: {correct_text}"
        )

    step += 1
    await update_state(callback.from_user.id, q_idx=step, ok_count=ok_count)

    if step < len(quiz_data):
        await ask(callback, callback.from_user.id)
    else:
        total = len(quiz_data)
        percent = round((ok_count / total) * 100)
        await callback.message.answer(
            f"Конец!\nВаш результат: {ok_count}/{total} верных ({percent}%)"
        )

def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_quiz, Command("quiz"))
    dp.message.register(cmd_quiz, F.text == "Начать игру")
    dp.callback_query.register(handle_answer)