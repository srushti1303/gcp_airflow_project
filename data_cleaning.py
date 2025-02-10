import pandas as pd
import re

# Load datasets
stock_df = pd.read_csv("stock_data.csv")  # Stock market prices
tweets_df = pd.read_csv("twitter_finance_data.csv")  # Social media tweets
news_df = pd.read_csv("financial_news.csv")  # Financial news articles

# Convert date columns to datetime format
stock_df["Date"] = pd.to_datetime(stock_df["Date"])
tweets_df["Created At"] = pd.to_datetime(tweets_df["Created At"])
news_df["published_at"] = pd.to_datetime(news_df["published_at"])

# Fill missing values in stock data with forward fill
stock_df.fillna(method="ffill", inplace=True)

# Drop tweets or news articles with missing text
tweets_df.dropna(subset=["Text"], inplace=True)
news_df.dropna(subset=["description"], inplace=True)

# Clean text: remove URLs, special characters
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)  # Remove links
    text = re.sub(r'\@w+|\#','', text)  # Remove mentions and hashtags
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text

tweets_df["Cleaned_Text"] = tweets_df["Text"].apply(clean_text)
news_df["Cleaned_Description"] = news_df["description"].apply(clean_text)

# Save cleaned data
stock_df.to_csv("cleaned_stock_data.csv", index=False)
tweets_df.to_csv("cleaned_twitter_data.csv", index=False)
news_df.to_csv("cleaned_financial_news.csv", index=False)

print("✅ Data cleaning completed. Cleaned files saved.")
