import requests
from config import NEWS_API_KEY

def get_news():
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "category": "technology",
            "language": "ru",
            "apiKey": NEWS_API_KEY,
            "pageSize": 3,
        }
        res = requests.get(url, params=params)
        data = res.json()
        articles = data.get("articles", [])
        if not articles:
            return "Новостей не найдено."
        result = []
        for a in articles:
            result.append(f"📰 {a['title']}\n{a['url']}")
        return "\n\n".join(result)
    except:
        return "Ошибка при получении новостей."
