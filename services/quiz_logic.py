# services/quiz_logic.py
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.db import get_quiz_index
from data.questions import quiz_data

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()
    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=option  # Передаём текст как callback_data
        ))
    builder.adjust(1)
    return builder.as_markup()


async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    question = quiz_data[current_question_index]
    correct_text = question['options'][question['correct_option']]
    kb = generate_options_keyboard(question['options'], correct_text)
    await message.answer(question['question'], reply_markup=kb)