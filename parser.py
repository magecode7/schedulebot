import requests


# Функция для получения расписания
def get_schedule(group_id: int, month: int, year: int) -> dict:
    url = f"https://apeksvuz.krdumvd.ru/api/call/schedule-schedule/student?token=fcf2d4e9-d241-7821-2c5b-df9a7f9f96d2&group_id={group_id}&month={month}&year={year}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        return None
