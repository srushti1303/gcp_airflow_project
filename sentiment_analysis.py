import pandas as pd

# Load datasets
stock_df = pd.read_csv("cleaned_stock_data.csv",parse_dates=["Date"])
tweets_df = pd.read_csv("tweets_sentiment_ner.csv", parse_dates=["Date"])
news_df = pd.read_csv("news_sentiment_ner.csv", parse_dates=["Date"])

print("✅ Data Loaded Successfully.")

# Convert dates to YYYY-MM-DD format for consistency
tweets_df["Date"] = tweets_df["Date"].dt.date
news_df["Date"] = news_df["Date"].dt.date
stock_df["Date"] = stock_df["Date"].dt.date

# Aggregate tweet sentiment per day
daily_tweet_sentiment = tweets_df.groupby("Date")["Sentiment_Score"].mean().reset_index()
daily_tweet_sentiment.rename(columns={"Date": "Date", "Sentiment_Score": "Tweet_Sentiment"}, inplace=True)

# Aggregate news sentiment per day
daily_news_sentiment = news_df.groupby("Date")["Sentiment_Score"].mean().reset_index()
daily_news_sentiment.rename(columns={"Date": "Date", "Sentiment_Score": "News_Sentiment"}, inplace=True)

# Merge stock data with tweet sentiment
stock_sentiment_df = stock_df.merge(daily_tweet_sentiment, on="Date", how="left")

# Merge with news sentiment
stock_sentiment_df = stock_sentiment_df.merge(daily_news_sentiment, on="Date", how="left")

# Fill NaN values with 0 (neutral sentiment)
stock_sentiment_df.fillna(0, inplace=True)

print("✅ Sentiment Data Merged with Stock Prices.")


stock_sentiment_df.to_csv("financial_analysis.csv", index=False)

