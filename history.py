import json
import os


def load_history():

    if os.path.exists("chat_history.json"):

        with open("chat_history.json", "r", encoding="utf-8") as file:
            return json.load(file)

    else:
        return []


def save_history(history):

    with open("chat_history.json", "w", encoding="utf-8") as file:
        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
        )