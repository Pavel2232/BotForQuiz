from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_quiz_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text='Новый вопрос'))
    builder.add(KeyboardButton(text='Сдаться'))
    builder.add(KeyboardButton(text='Мой счёт'))

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
