import random

from pyexpat.errors import messages
from supabase import Client, create_client
from sys import excepthook
from config import url,key
import secrets
import asyncio
from config import token
from aiogram import*
from aiogram.filters import CommandStart, Command
from aiogram.types import BotCommand

supabase : Client = create_client(url,key)

bot = Bot(token=token)
dp = Dispatcher()
welcome_text = ("<b>👋 Привет! Добро пожаловать в Рандомус Бот!</b> 🎲\n\n"
    "Здесь ты можешь:\n"
    "🎯 Выбрать случайное число — просто напиши /random и укажи диапазон.\n"
    "🎲 Потянуть жребий — выбери участника из группы или список вариантов.\n"
    "⚡ Быстро принять решение — когда не можешь выбрать сам.\n\n"
    "Напиши /help, чтобы узнать все команды и начать играть!\n\n"
    "Готов? <b> Поехали! </b> 🚀")
# а
help_answer = (
    "📚 Помощь — команды бота\n\n"
    "<b>/start</b> — Запустить бота и получить приветствие 👋\n"
    "<b>/random [min] [max]</b> — Выбрать случайное число в диапазоне от min до max 🎲\n"
    "<b>/lottery [варианты через запятую]</b> — Потянуть жребий из списка вариантов 🎟️\n"
    "<b>/coinflip</b> - Подбросить монетку! 🪙 \n"
    "<b>/id</b> - Узнать информацию о пользователе 👨\n"
    "<b>/dice</b> - Бросить кубик"
    "<b>/help</b> — Показать это сообщение с командами ℹ️\n\n"
    "Пример:\n"
    "<b>/random 1 100</b> — выберет число от 1 до 100\n"
    "<b>/lottery яблоко банан груша</b> — выберет случайный фрукт из списка\n\n"
    "Если хочешь предложить идею или сообщить об ошибке — пиши сюда: @yatogotsirka\n\n"
    "Удачи и пусть фортуна будет на твоей стороне! 🍀"
)


@dp.message(CommandStart()) # хендлер слушает и ждет сообщение
async def cmd_start(message):
    await message.answer(welcome_text,parse_mode = 'HTML')
    try:
        response = supabase.table('randombot').insert({'telegram_id': message.from_user.username}).execute()
    except Exception as error:
        print(error)
@dp.message(Command('help'))
async def cmd_help(message):
    await message.answer(help_answer, parse_mode = 'HTML')
@dp.message(Command('coinflip'))
async def cmd_coinflip(message):
    await message.answer('Выпал Орел! 🦅 (50%)' if secrets.randbelow(2)==1 else 'Выпала Решка! 💰 (50%)')
@dp.message(Command('random'))
async def cmd_random(message):
    args = message.text.split()[1:]
    args = list(map(int,args))
    if len(args)==2:
        if args[0] > args[1]:
            await message.answer(f'{random.randint(args[1],args[0])}')
        else:
            await message.answer(f'{random.randint(args[0],args[1])}')
    else:
        await message.answer('❗ Используй формат: <b>/random [min] [max]</b>\nПример: <b>/random 1 100</b>', parse_mode='HTML')


@dp.message(Command('lottery'))
async def cmd_lottery(message):
    args = message.text.split()[1:]
    if len(args)==2:
        await message.answer(f'Вам выпало: {secrets.choice(args)} ' )
    else:
        await message.answer(
            '❗ Используй формат: <b>/lottery вариант1 вариант2 .... вариант100</b>\n Пример: <b>/lottery Женя Коля Артём</b>',parse_mode='HTML')

@dp.message(F.text == 'Привет!') # в F.text хранится сообщение от пользователя и мы его сравниваем
async def cmd_hello(message):
    await message.answer('Привет! Если не сложно, поделись этим ботом с друзьями!')

@dp.message(F.sticker)
async def sticker_response(message):
    await message.answer('😂')

@dp.message(Command('id'))
async def cmd_id(message):
    await message.answer(
    f"🆔 <b>Ваш Айди:</b> {message.from_user.id}\n"
    f"👤 <b>Имя:</b> {message.from_user.first_name}\n"
    f"👥 <b>Фамилия:</b> {message.from_user.last_name or '—'}\n"
    f"🔗 <b>Юзернейм:</b> @{message.from_user.username or 'нет'}\n"
    f"🌟 <b>Телеграм Премиум:</b> {message.from_user.is_premium}",
    parse_mode="HTML"
)

@dp.message(Command('dice'))
async def cmd_dice(message):
    dice = await message.answer_dice(emoji='🎲') # кинуть дайс, тут либо кубик, либо дартс либо баскет кольцо
    await asyncio.sleep(5)
    await message.answer(f'🔥 Вам выпало - {dice.dice.value}!')

async def main():
    print('connection success')
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота 👋"),
        BotCommand(command="help", description="Список команд ℹ️"),
        BotCommand(command="random", description="Случайное число 🎲"),
        BotCommand(command="lottery", description="Тянуть жребий 🎟️"),
        BotCommand(command="coinflip", description="Орел или решка 🪙"),
        BotCommand(command="dice", description="Бросить кубик 🎲"),
        BotCommand(command="id", description="Узнать информацию о себе 🆔"),
    ])
    await dp.start_polling(bot)




if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit ')
    print('играем')