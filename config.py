import os

# Токен группы ВК (Group Access Token) — из переменных окружения Railway или локального .env
BOT_TOKEN = os.getenv("VK_GROUP_TOKEN")

# Токен подтверждения Callback API ВК
CONFIRMATION_TOKEN = os.getenv("VK_CONFIRMATION_TOKEN")

# Ваш ВК ID — ваш ID ВКонтакте, например: 123456789
OWNER_ID = int(os.getenv("VK_OWNER_ID", "0"))

# ID группы ВКонтакте
GROUP_ID = int(os.getenv("VK_GROUP_ID", "0"))

# Имя бота для распознавания упоминаний (нижний регистр)
BOT_NAME = os.getenv("BOT_NAME", "dizel").lower()

# Порт для Flask
PORT = int(os.getenv("PORT", 8080))

# Ключ OpenAI для ChatGPT (бесплатный ключ с сайта openai.com)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ключи для API погоды и новостей (зарегистрируйтесь на openweathermap.org и newsapi.org)
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Путь к SQLite базе
DB_PATH = "core/db.sqlite3"
