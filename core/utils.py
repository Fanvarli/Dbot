import requests
from config import BOT_TOKEN, OWNER_ID
import logging

API_VERSION = "5.131"
VK_API_URL = "https://api.vk.com/method/"

def send_message(peer_id, message, keyboard=None, attachment=None):
    params = {
        "peer_id": peer_id,
        "message": message,
        "access_token": BOT_TOKEN,
        "v": API_VERSION,
        "random_id": 0,
    }
    if keyboard:
        params["keyboard"] = keyboard
    if attachment:
        params["attachment"] = attachment
    try:
        r = requests.post(VK_API_URL + "messages.send", params=params)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logging.error(f"Ошибка отправки сообщения: {e}")
        return None

def is_owner(user_id):
    return user_id == OWNER_ID

def parse_command(text, bot_name):
    # Удаляет упоминания бота, оставляет команду и аргументы
    text = text.lower()
    text = text.replace(bot_name, "").replace(f"@{bot_name}", "").strip()
    if text.startswith("!"):
        parts = text[1:].split()
        cmd = parts[0]
        args = parts[1:]
        return cmd, args
    return "", []
