import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import datetime
import config
import builder
import group_manager
import parser

commands = [
    types.BotCommand(command="start", description="Запуск бота"),
    types.BotCommand(command="help", description="Справка по командам"),
    types.BotCommand(command="group", description="Текущая группа"),
    types.BotCommand(command="today", description="Расписание на сегодня"),
    types.BotCommand(command="tommorow", description="Расписание на завтра"),
    types.BotCommand(command="week", description="Расписание на неделю"),
]

# Настройка логирования
logging.basicConfig(level=logging.INFO)

main_bot = Bot(token=config.config["TOKEN"])
dp = Dispatcher()


async def send_daily_schedule():
    while True:
        now = datetime.datetime.now()
        if now.hour == 6:  # Проверяем, 6 ли утра
            for chat_id, group_id in group_manager.get_chat_groups().items():
                schedule = parser.get_schedule(group_id, now.month, now.year)
                if schedule:
                    text = builder.get_lessons_text(schedule, now.date())
                    await main_bot.send_message(chat_id, text)

            await asyncio.sleep(60 * 60)  # Ждём час перед повторной проверкой
        await asyncio.sleep(60)  # Проверяем каждую минуту


# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await main_bot.set_my_commands(commands)
    await main_bot.send_message(
        message.chat.id,
        f"Привет {message.from_user.full_name}! Я бот, который покажет тебе расписание на сегодня. Используй команду /today.",
    )


# Обработчик команды /group
@dp.message(Command("group"))
async def set_group(message: types.Message):
    split = message.text.split()
    group_name = group_manager.get_group_name(str(message.chat.id))
    if len(split) < 2:
        if group_name:
            await main_bot.send_message(message.chat.id, f"Текущая группа {group_name}")
            return
        else:
            await main_bot.send_message(
                message.chat.id,
                "Не указана группа. Используй команду /group [название группы]",
            )
            return
    else:
        group_name = split[1]
        success = group_manager.add_group(str(message.chat.id), group_name)
        if not success:
            await main_bot.send_message(
                message.chat.id,
                "Данная группа не найдена. Попробуйте еще раз.",
            )
        else:
            await main_bot.send_message(
                message.chat.id, f"Установлена группа {group_name}"
            )


# Обработчик команды /today
@dp.message(Command("today"))
async def send_today_schedule(message: types.Message):
    today = datetime.date.today()
    group_id = group_manager.get_group_id(str(message.chat.id))
    month = today.month
    year = today.year

    if not group_id:
        await main_bot.send_message(
            message.chat.id,
            "Не указана группа. Используй команду /group [название группы]",
        )
        return

    schedule = parser.get_schedule(group_id, month, year)
    if schedule:
        text = builder.get_lessons_text(schedule, today)
        await main_bot.send_message(message.chat.id, text)
    else:
        await main_bot.send_message(
            message.chat.id, "Не удалось получить расписание. Попробуйте позже."
        )


# Обработчик команды /tommorow
@dp.message(Command("tommorow"))
async def send_tommorow_schedule(message: types.Message):
    tommorow = datetime.date.today() + datetime.timedelta(days=1)
    group_id = group_manager.get_group_id(str(message.chat.id))
    month = tommorow.month
    year = tommorow.year

    if not group_id:
        await main_bot.send_message(
            message.chat.id,
            "Не указана группа. Используй команду /group [название группы]",
        )
        return

    schedule = parser.get_schedule(group_id, month, year)
    if schedule:
        text = builder.get_lessons_text(schedule, tommorow)
        await main_bot.send_message(message.chat.id, text)
    else:
        await main_bot.send_message(
            message.chat.id, "Не удалось получить расписание. Попробуйте позже."
        )


# Обработчик команды /date
@dp.message(Command("date"))
async def send_day_schedule(message: types.Message):
    split = message.text.split()
    if len(split) < 2:
        await main_bot.send_message(
            message.chat.id,
            "Не указана дата. Используй команду /date <01.01.2000>",
        )
        return
    date = split[1]
    day = datetime.datetime.strptime(date, "%d.%m.%Y").date()
    group_id = group_manager.get_group_id(str(message.chat.id))
    month = day.month
    year = day.year

    if not group_id:
        await main_bot.send_message(
            message.chat.id,
            "Не указана группа. Используй команду /group [название группы]",
        )
        return

    schedule = parser.get_schedule(group_id, month, year)
    if schedule:
        text = builder.get_lessons_text(schedule, day)
        await main_bot.send_message(message.chat.id, text)
    else:
        await main_bot.send_message(
            message.chat.id, "Не удалось получить расписание. Попробуйте позже."
        )


# Обработчик команды /now
@dp.message(Command("now"))
async def send_now_schedule(message: types.Message):
    now = datetime.datetime.now()
    await main_bot.send_message(message.chat.id, now.strftime("%d.%m.%Y %H:%M"))


# Обработчик команды /groups
@dp.message(Command("groups"))
async def send_groups(message: types.Message):
    group_names = group_manager.get_group_names()
    text = "Список групп:\n"
    for group_name in group_names.values():
        text += f"{group_name}\n"
    if len(text) > 4096:
        for i in range(0, len(text), 4096):
            await main_bot.send_message(message.chat.id, text[i : i + 4096])
    else:
        await main_bot.send_message(message.chat.id, text)


# Обработчик команды /week
@dp.message(Command("week"))
async def send_week_schedule(message: types.Message):
    week = datetime.date.today()
    group_id = group_manager.get_group_id(str(message.chat.id))
    month = week.month
    year = week.year

    if not group_id:
        await main_bot.send_message(
            message.chat.id,
            "Не указана группа. Используй команду /group [название группы]",
        )
        return

    schedule = parser.get_schedule(group_id, month, year)
    if schedule:
        text = builder.get_week_lessons_text(schedule, week)
        await main_bot.send_message(message.chat.id, text)
    else:
        await main_bot.send_message(
            message.chat.id, "Не удалось получить расписание. Попробуйте позже."
        )


# Обработчик команды /help
@dp.message(Command("help"))
async def send_help(message: types.Message):
    await main_bot.send_message(
        message.chat.id,
        "Список команд:\n/start - начало работы с ботом\n/group - установка группы\n/today - расписание на сегодня\n/tommorow - расписание на завтра\n/date - расписание на указанную дату\n/week - расписание на неделю\n/groups - список групп\n/help - помощь",
    )


# Запуск бота
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(send_daily_schedule())
    loop.run_until_complete(dp.start_polling(main_bot))
