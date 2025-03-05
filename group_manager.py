import json
import parser
import datetime
import os

chat_groups = {}
group_names = {}

if not os.path.exists("chat_groups.json"):
    with open("chat_groups.json", "w") as f:
        json.dump(chat_groups, f)
else:
    with open("chat_groups.json", "r") as f:
        chat_groups = json.load(f)

today = datetime.date.today()
month = today.month
year = today.year

group_names = parser.get_schedule(1, month, year)["groupNames"]


def add_group(chat_id: str, group_name: str) -> bool:
    group_id = 0
    for k, v in group_names.items():
        if v == group_name:
            group_id = k
            break
    if group_id == 0:
        return False
    chat_groups[str(chat_id)] = group_id
    with open("chat_groups.json", "w") as f:
        json.dump(chat_groups, f)
    return True


def get_group_name(chat_id: str):
    return group_names.get(chat_groups.get(str(chat_id), 0), "")


def get_group_id(chat_id: str):
    return chat_groups.get(str(chat_id), 0)


def get_chat_groups():
    return chat_groups


def get_group_names():
    return group_names
