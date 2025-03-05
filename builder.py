import datetime


def get_lessons_text(data: dict, date: datetime.date):
    text = ""

    lessons = data.get("lessons", [])

    date_str = date.strftime("%d.%m.%Y")
    schedule = [lesson for lesson in lessons if lesson["date"] == date_str]
 
    if not schedule:
        return "Расписание на данный день не найдено"

    # Сортируем по lesson_time_id
    schedule.sort(key=lambda lesson: lesson["lesson_time_id"])

    text += f"Расписание на {date_str}\n\n"
    for lesson in schedule:
        text += f"{lesson['lesson_time_id']}) {lesson['discipline']} {lesson['class_type_name']} | {lesson.get('classroom', 'Не указано')} | {', '.join(lesson.get('staffNames', []))}\n"

    return text
