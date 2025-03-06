import datetime

day_of_week_ru = {
    "Monday": "Понедельник",
    "Tuesday": "Вторник",
    "Wednesday": "Среда",
    "Thursday": "Четверг",
    "Friday": "Пятница",
    "Saturday": "Суббота",
    "Sunday": "Воскресенье",
}


def get_lessons_text(data: dict, date: datetime.date):
    text = ""

    lessons = data.get("lessons", [])

    date_str = date.strftime("%d.%m.%Y")
    schedule = [lesson for lesson in lessons if lesson["date"] == date_str]

    if not schedule:
        return "Расписание на данный день не найдено"

    # Сортируем по lesson_time_id
    schedule.sort(key=lambda lesson: lesson["lesson_time_id"])
    day_of_week = date.strftime("%A")

    text += f"Расписание на {date_str} ({day_of_week_ru[day_of_week]})\n\n"
    for lesson in schedule:
        text += f"{lesson['lesson_time_id']}) {lesson['discipline']} {lesson['class_type_name']} | {lesson.get('classroom', 'Не указано')} | {', '.join(lesson.get('staffNames', []))}\n"

    return text


def get_week_lessons_text(data: dict, date: datetime.date):
    week_start_date = date - datetime.timedelta(days=date.weekday())
    week_end_date = week_start_date + datetime.timedelta(days=6)

    lessons = data.get("lessons", [])

    day_schedules = {}
    for lesson in lessons:
        date_str = lesson["date"]
        if (
            week_start_date
            <= datetime.datetime.strptime(date_str, "%d.%m.%Y").date()
            <= week_end_date
        ):
            day_schedules[date_str] = day_schedules.get(date_str, []) + [lesson]

    text = "Расписание на неделю\n\n"
    for date_str in sorted(day_schedules.keys()):
        date = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()
        day_of_week = date.strftime("%A")
        text += f"Расписание на {date_str} ({day_of_week_ru[day_of_week]})\n\n"
        for lesson in day_schedules[date_str]:
            text += f"{lesson['lesson_time_id']}) {lesson['discipline']} {lesson['class_type_name']} | {lesson.get('classroom', 'Не указано')} | {', '.join(lesson.get('staffNames', []))}\n"
        text += "\n"

    return text
