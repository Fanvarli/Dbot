import requests
from config import WEATHER_API_KEY

def get_weather(city):
    try:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric",
            "lang": "ru"
        }
        res = requests.get(url, params=params)
        data = res.json()
        if data.get("cod") != 200:
            return "Город не найден."
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"Погода в {city.title()}: {desc}, температура {temp}°C."
    except:
        return "Ошибка при получении погоды."
