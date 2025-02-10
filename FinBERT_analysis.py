import pandas as pd
import torch
from transformers import pipeline
import spacy

# Load datasets
tweets_df = pd.read_csv("cleaned_twitter_data.csv")
news_df = pd.read_csv("cleaned_financial_news.csv")

# Convert necessary columns to strings
tweets_df["Text"] = tweets_df["Text"].astype(str)
news_df["Cleaned_Description"] = news_df["Cleaned_Description"].astype(str)

# Load FinBERT sentiment analysis pipeline
sentiment_pipeline = pipeline("text-classification", model="ProsusAI/finbert")

# Function to analyze sentiment
def analyze_sentiment(text):
    if not isinstance(text, str) or text.strip() == "":
        return "Neutral"  # If text is empty or NaN, default to Neutral
    result = sentiment_pipeline(text[:512])[0]  # Limit to 512 tokens for BERT
    return result["label"]

# Apply sentiment analysis to tweets
tweets_df["Sentiment"] = tweets_df["Text"].apply(analyze_sentiment)

# Apply sentiment analysis to news
news_df["Sentiment"] = news_df["Cleaned_Description"].apply(analyze_sentiment)

print("✅ Sentiment Analysis Completed.")

# Mapping function
sentiment_map = {"positive": 1, "neutral": 0, "negative": -1}

# Apply mapping to tweets
tweets_df["Sentiment_Score"] = tweets_df["Sentiment"].str.lower().map(sentiment_map)

# Apply mapping to news
news_df["Sentiment_Score"] = news_df["Sentiment"].str.lower().map(sentiment_map)

# Load spaCy model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

# Function to extract entities from text
def extract_entities(text):
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "GPE", "MONEY", "PERSON"]]
    return ", ".join(entities) if entities else "None"

# Apply NER to tweets
tweets_df["Entities"] = tweets_df["Text"].apply(extract_entities)

# Apply NER to news
news_df["Entities"] = news_df["Cleaned_Description"].apply(extract_entities)


tweets_df.to_csv("tweets_sentiment_ner.csv", index=False)
news_df.to_csv("news_sentiment_ner.csv", index=False)
