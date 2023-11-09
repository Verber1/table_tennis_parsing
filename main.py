import sys
sys.path.insert(0, '/src/')
from src import TableTennisParsing
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from time import sleep

# Считываем токен
f = open('token.txt', 'r')
token = f.readline()

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=token)
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    #await message.answer("Hello!")
    while True:
        #output_value = TableTennisParsing.test_work()
        output_text_res = TableTennisParsing.main()
        for text_res in output_text_res:
            await message.answer(text_res)
        sleep(5)

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

