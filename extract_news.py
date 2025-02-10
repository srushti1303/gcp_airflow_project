from newsapi import NewsApiClient
import pandas as pd

# NewsAPI Key (Get yours from https://newsapi.org/)
NEWS_API_KEY = "your-api"

# Initialize API client
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# Fetch financial news (top headlines related to finance)
articles = newsapi.get_top_headlines(category="business", language="en", country="us")

# Extract relevant fields
news_data = []
for article in articles["articles"]:
    news_data.append({
        "title": article["title"],
        "source": article["source"]["name"],
        "published_at": article["publishedAt"],
        "url": article["url"],
        "description": article["description"]
    })

# Convert to DataFrame
df_news = pd.DataFrame(news_data)

# Save to CSV
df_news.to_csv("financial_news.csv", index=False)
print("Financial News Data Saved: financial_news.csv")
