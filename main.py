import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import requests
import datetime
import config
import builder

commands = [
    types.BotCommand(command="start", description="Запуск бота"),
    types.BotCommand(command="today", description="Расписание на сегодня"),
    types.BotCommand(command="tommorow", description="Расписание на завтра"),
]

# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
bot.set_my_commands(commands)
dp = Dispatcher()


# Функция для получения расписания
def get_schedule(group_id: int, month: int, year: int) -> dict:
    url = f"https://apeksvuz.krdumvd.ru/api/call/schedule-schedule/student?token=fcf2d4e9-d241-7821-2c5b-df9a7f9f96d2&group_id={group_id}&month={month}&year={year}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        return None


async def send_daily_schedule():
    while True:
        now = datetime.datetime.now()
        if now.hour == 6:  # Проверяем, 6 ли утра
            schedule = get_schedule(config.VZVOD_ID, now.month, now.year)
            if schedule:
                text = builder.get_lessons_text(schedule, now.date())
                await bot.send_message(config.GROUP_ID, text)

            await asyncio.sleep(60 * 60)  # Ждём час перед повторной проверкой
        await asyncio.sleep(60)  # Проверяем каждую минуту


# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await bot.send_message(
        message.chat.id,
        f"Привет {message.from_user.full_name}! Я бот, который покажет тебе расписание на сегодня. Используй команду /today.",
    )


# Обработчик команды /schedule
@dp.message(Command("today"))
async def send_today_schedule(message: types.Message):
    today = datetime.date.today()
    group_id = config.VZVOD_ID
    month = today.month
    year = today.year

    schedule = get_schedule(group_id, month, year)
    if schedule:
        text = builder.get_lessons_text(schedule, today)
        await message.reply(text)
    else:
        await message.reply("Не удалось получить расписание. Попробуйте позже.")


# Обработчик команды /tommorow
@dp.message(Command("tommorow"))
async def send_tommorow_schedule(message: types.Message):
    tommorow = datetime.date.today() + datetime.timedelta(days=1)
    group_id = config.VZVOD_ID
    month = tommorow.month
    year = tommorow.year

    schedule = get_schedule(group_id, month, year)
    if schedule:
        text = builder.get_lessons_text(schedule, tommorow)
        await message.reply(text)
    else:
        await message.reply("Не удалось получить расписание. Попробуйте позже.")


# Запуск бота
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(send_daily_schedule())
    loop.run_until_complete(dp.start_polling(bot))
