from aiogram import*
import asyncio
import os

from supabase import create_client,Client
from aiogram.filters import CommandStart
from aiohttp.helpers import TOKEN
from config import tokenInfo, key,url

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
tokenInfo = os.getenv("INFO_TOKEN")

bot = Bot(token=tokenInfo) # иниц бота
dp = Dispatcher()

supabase: Client = create_client(url, key) # сапабейс как экземпляр класса Client из библиотеки

@dp.message(CommandStart)
async def cmd_id(message):
    await message.answer(
    f"🆔 <b>Ваш Айди:</b> {message.from_user.id}\n"
    f"👤 <b>Имя:</b> {message.from_user.first_name}\n"
    f"👥 <b>Фамилия:</b> {message.from_user.last_name or '—'}\n"
    f"🔗 <b>Юзернейм:</b> @{message.from_user.username or 'нет'}\n"
    f"🌟 <b>Телеграм Премиум:</b> {message.from_user.is_premium}",
    parse_mode="HTML"
)
    try:
        
        response = supabase.table('yourId').insert({'telegram_id': message.from_user.username}).execute()
    except Exception as error:
        print('DB ERROR:', error)


async def main():
    print('startup success')
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit ')
