import requests
import config
import datetime
import json
import builder

today = datetime.date.today()
group_id = config.VZVOD_ID
month = today.month
year = today.year

url = f"https://apeksvuz.krdumvd.ru/api/call/schedule-schedule/student?token=fcf2d4e9-d241-7821-2c5b-df9a7f9f96d2&group_id={group_id}&month={month}&year={year}"
response = requests.get(url)

print(builder.get_lessons_text(response.json()["data"], today))
