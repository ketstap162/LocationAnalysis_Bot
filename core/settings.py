import os

# DEBUG
DEBUG = True

if DEBUG:
    from dev_tools.environment import env_setup
    env_setup()

# ENV

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
LOCATIONS = ["Київ", "Харків", "Львів", "Днепр", "Вінниця"]
QUESTIONS = ["Питання 1", "Питання 2", "Питання 3", "Питання 4", "Питання 5"]

TELEGRAM_FILE_STORAGE_URL = f"https://api.telegram.org/file/bot{BOT_TOKEN}/"


if __name__ == "__main__":
    attributes = globals().copy()
    for name, value in attributes.items():
        print(f"{name} = {value}")
