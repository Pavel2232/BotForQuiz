import asyncio
import logging
from aiogram.filters import CommandStart
from aiogram import F
from settings import dp, bot



async def main() -> None:
    dp.message.register(command_start_handler, CommandStart())
    dp.message.register(get_new_question_handler, F.text == 'Новый вопрос')
    dp.message.register(conversation_handler, F.text == 'Сдаться')
    dp.message.register(check_answer_handler)
    await dp.start_polling(bot)


if __name__ == "__main__":
    from handlers.commands import command_start_handler, get_new_question_handler, check_answer_handler, \
        conversation_handler
    logging.getLogger('BotTG')
    asyncio.run(main())
