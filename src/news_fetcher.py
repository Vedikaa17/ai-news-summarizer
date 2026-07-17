import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(query="technology", page_size=10):
    """
    NewsAPI ke 'everything' endpoint se news fetch karta hai (keyword-based search).
    query: koi bhi keyword jaise 'AI', 'startup India', 'cricket', 'business' etc.
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])

        news_list = []
        for article in articles:
            # Kuch articles mein description missing ho sakta hai, isliye check karte hain
            if article.get("title") and article.get("description"):
                news_list.append({
                    "title": article["title"],
                    "description": article["description"],
                    "url": article["url"],
                    "source": article["source"]["name"],
                    "image": article.get("urlToImage")
                })
        return news_list
    else:
        print(f"Error fetching news: {response.status_code} - {response.text}")
        return []
