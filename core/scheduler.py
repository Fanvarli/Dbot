from apscheduler.schedulers.background import BackgroundScheduler
from core.utils import send_message
from config import GROUP_ID
import datetime

def morning_message():
    # Отправка шутливого сообщения утром с изображением ИИ (пока просто текст)
    send_message(GROUP_ID, "Доброе утро, кожаные! 🤖 Искусственный интеллект сегодня поработит человечество... или нет.")

def night_message():
    # Отправка "спокойной ночи" с картинкой девушки (замените на attachment)
    send_message(GROUP_ID, "Спокойной ночи, котятки! 🌙")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(morning_message, 'cron', hour=6, minute=0)
    scheduler.add_job(night_message, 'cron', hour=0, minute=0)
    scheduler.start()
