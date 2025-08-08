from flask import Flask, request
from config import *
from core.handlers import handle_event
from core.scheduler import start_scheduler
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['POST'])
def vk_callback():
    data = request.json
    if data is None:
        return "ok"

    # Подтверждение сервера VK (confirmation)
    if data.get('type') == 'confirmation':
        return CONFIRMATION_TOKEN

    # Новое сообщение
    if data.get('type') == 'message_new':
        handle_event(data)
        return 'ok'

    return 'ok'

if __name__ == '__main__':
    start_scheduler()  # Запускаем планировщик для авто-сообщений
    app.run(host='0.0.0.0', port=PORT)
