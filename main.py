import sys
sys.path.insert(0, '/src/')
from src import TableTennisParsing
import variables # модуль с переменными из config.ini
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from time import sleep
import time

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=variables.TOKEN_BOT)
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def bot_start_command(message: types.Message):
    #await message.answer("Hello!")
    await message.answer('Запуск...')

# Хэндлер проверки, что бот работает
@dp.message(Command("status"))
async def bot_status_command(message: types.Message):
    await message.answer('Бот работает!')

# Вывести chat id
@dp.message(Command("chat_id"))
async def get_chat_id(message: types.Message):
    chat_id_curr = message.chat.id
    await message.reply(f"Chat id для этого чата: {chat_id_curr}")

# Основная функция для парсинга и анализа результатов
async def parsing_matches():
    while True:
        output_text_res = TableTennisParsing.main()
        for chat_id in variables.CHAT_ID:
            for text_res in output_text_res:
                await bot.send_message(chat_id, text_res)

        await asyncio.sleep(5) # Общее время одного прохода с учетом sleep занимает ~15 секунд

# Запуск процесса поллинга новых апдейтов
async def main():
    await asyncio.gather(dp.start_polling(bot), parsing_matches())

if __name__ == '__main__':
    asyncio.run(main())

